"""Parsing code for DICOMS and contour files"""

import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd
import os 
from patientClass import Patient 
import save
import h5py
import random
import path_settings as ps
import matplotlib.pyplot as plt 



def parse_contour_file(filename):
    """Parse the given contour filename

    :param filename: filepath to the contourfile to parse
    :return: list of tuples holding x, y coordinates of the contour
    """

    coords_lst = []
    
    # modification: add try and except for corrupt/not existing file
    try:
        with open(filename, 'r') as infile:
            for line in infile:
                coords = line.strip().split()

                x_coord = float(coords[0])
                y_coord = float(coords[1])
                coords_lst.append((x_coord, y_coord))

            return coords_lst

    except FileNotFoundError:
        print("Path to be parsed was not found.")   
        return None 
    except TypeError:
        print("Path is None Type.")
        return None
    except Exception as e:
        print(e)
        return None
        

def parse_dicom_file(filename):
    """Parse the given DICOM filename

    :param filename: filepath to the DICOM file to parse
    :return: dictionary with DICOM image data
    """

    try:
        dcm = pydicom.read_file(filename)
        dcm_image = dcm.pixel_array

        try:
            intercept = dcm.RescaleIntercept
        except AttributeError:
            intercept = 0.0
        try:
            slope = dcm.RescaleSlope
        except AttributeError:
            slope = 0.0

        if intercept != 0.0 and slope != 0.0:
            dcm_image = dcm_image*slope + intercept
        dcm_dict = {'pixel_data' : dcm_image}
        return dcm_dict
    except InvalidDicomError:
        return None
    except:
        print(" Problem reading DICOM file.")


def poly_to_mask(polygon, width, height):
    """Convert polygon to mask

    :param polygon: list of pairs of x, y coords [(x1, y1), (x2, y2), ...]
     in units of pixels
    :param width: scalar image width
    :param height: scalar image height
    :return: Boolean mask of shape (height, width)
    """

    # http://stackoverflow.com/a/3732128/1410871
    img = Image.new(mode='L', size=(width, height), color=0)
    ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
    mask = np.array(img).astype(bool)
    return mask



def generate_input_target_arrays(linkfile):
    """ pipeline to generate the input and target arrays 

    :return: tuple of np.arrays for input and target data
    """

    targets = []
    inputs = []

    patient_original_id_mapping = link_patient_contour_id(linkfile)

    # iterate over all patients 
    for patient_id, original_id in patient_original_id_mapping.items():
        patient = Patient(patient_id,original_id)
        dicom_contour_mapping = patient.map_dicom_contour()

        # iterate through valid dicom and contour pairs 
        for dicom, contour in dicom_contour_mapping.items():
            dicom_pixel_data = parse_dicom_file(patient.dicom_path+"/"+dicom)

            # TODO replace quickfix for handling corrupt string
            contour = contour.strip("._")

            # apply parsing functions to obtain target and input arrays 
            contour_tuples = parse_contour_file(patient.contour_path+"/"+contour)
            height, width = dicom_pixel_data["pixel_data"].shape
            mask = poly_to_mask(contour_tuples, height, width)
            
            # if visualization of mask is wanted
            # visualize_mask(mask, patient_id, dicom, save = True)

            targets.append(mask)
            inputs.append(dicom_pixel_data["pixel_data"])

    return np.array(inputs), np.array(targets)



def link_patient_contour_id(linkfile):
    """ function to create a mapping between patient_id and original_id

    :param link: path to csv file that contains the mapping between 
     patient_id (first column) and contour_id (second column)
    :return: dict containing patient_id as key and contour_id as item
    """
    try:
        file = pd.read_csv(linkfile)
        
        mapping = {}
        for idx in range(0,file.shape[0]):
            mapping[file.iloc[idx,0]]= file.iloc[idx,1]
        return mapping

    except FileNotFoundError:
        print("Path to Linkfile not found.")   
        return None 
    except TypeError:
        print("Path to Linkfile is None Type.")
        return None
    except Exception as e:
        print(e)
        return None



def visualize_mask(mask, patient_id = None, dicom = None,  save = False,):
    """ helper function to visualize the generated mask
        :param mask: boolean 2D array
        :param patient_id: string of patient id, optional for storing
        :param dicom: string of dicom number, optional for storing
        :param save: bool, optional, if storing of image is wanted
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(mask, aspect='auto', cmap=plt.cm.gray, interpolation='nearest')
    if save:
        plt.savefig('./data/'+patient_id+"_"+dicom+".png")

