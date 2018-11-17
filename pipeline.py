import parsing
import numpy as np 
import pandas as pd
import os 
import re
from patientClass import Patient 
import save
import h5py
import random


# paths for reuse throughout project
data_dir = "./data/dicoms/"
contour_type = "i-contours"
data_dir_con = "./data/contourfiles/"   




def pipe(linkfile):
    """ pipeline to generate the input and target arrays 

    :param linkfile: path to csv file containing the mapping of patient_id and original_id
    """

    targets = []
    inputs = []

    patient_original_id_mapping = link_patient_contour_id(linkfile)

    for patient_id, original_id in patient_original_id_mapping.items():
        patient = Patient(patient_id,original_id)
        dicom_contour_mapping = patient.map_dicom_contour()

        for dicom, contour in dicom_contour_mapping.items():
            dicom_pixel_data = parsing.parse_dicom_file(patient.dicom_path+"/"+dicom)

            # TODO replace quickfix for handling corrupt string
            contour = contour.strip("._")

            # apply parsing functions to obtain target and input arrays 
            contour_tuples = parsing.parse_contour_file(patient.contour_path+"/"+contour)
            height, width = dicom_pixel_data["pixel_data"].shape
            mask = parsing.poly_to_mask(contour_tuples, height, width)

            targets.append(mask)
            inputs.append(dicom_pixel_data["pixel_data"])

    return np.array(inputs), np.array(targets)


def link_patient_contour_id(linkfile):
    """ function to create a mapping between patient_id and original_id

    :param link: path to csv file that contains the mapping between patient_id (first column) and contour_id (second column)
    :return: dict containing patient_id as key and contour_id as item
    """
    try:
        file = pd.read_csv(linkfile)
        
        mapping = {}
        for idx in range(1,file.shape[0]):
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



class DataGenerator():

    def __init__(self,batchsize, input, target):
        self.batchsize = batchsize
        self.target = target
        self.input = input
        self.dim = input.shape[1]
        self.dataset_size = input.shape[0]
        self.indices = np.arange(self.dataset_size)

    def __len__(self):
        return int(np.floor(self.dataset_size / self.batchsize))

    def on_epoch_end(self):
        np.random.shuffle(self.indices)

    def __getitem__(self, idx):
        inds = self.indices[idx * self.batchsize:(idx + 1) * self.batchsize]
        input_batch = np.array(np.resize(input[inds], (self.batchsize,1,self.dim,self.dim,)))
        target_batch =  np.array(np.resize(target[inds], (self.batchsize,1,self.dim,self.dim)))
        return input_batch, target_batch


f = h5py.File('./data/processed_data.h5')
target = f['target'].value
input = f['input'].value
d = DataGenerator(8,input,target )
i =0
for x in d:
    i += 1
print(i)
#input,target = pipe('./data/link.csv')
#save.save_data(input,target)