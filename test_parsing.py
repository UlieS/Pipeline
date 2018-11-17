import unittest
import parsing 
import os 
import numpy as np
import pydicom
import matplotlib.pyplot as plt


class TestParsing(unittest.TestCase):

    def test_parse_contour_file(self):
        """
        Unittest for parse_contour_file() function
        tests for:
         - correct output data type 
         - output file includes all information from input file 
         - correct error handling when file not existant
        """
        contourtype = "i-contours"
        data_dir = "./data/contourfiles/"

        # tests all available data on the function
        for patient_dir in os.listdir(data_dir):
            file_path = os.path.join(data_dir,patient_dir+"/"+contourtype)

            for contour in os.listdir(file_path):   
                # TODO replace quickfix for corrupt filenames
                contourfile = file_path+"/"+contour.strip(".").strip("_")
              
                # generate output returned by the function to be tested
                output = parsing.parse_contour_file(contourfile)

                # test data type
                self.assertIsInstance(output, list)
                for element in output:
                    self.assertIsInstance(element, tuple)
                    x,y = element
                    self.assertIsInstance(x,float)
                    self.assertIsInstance(y,float)
                
                # test whether length of list is equal to file 
                contourfile_length = file_length(contourfile)
                self.assertEqual(len(output), contourfile_length)


        # test error handling
        self.assertRaises(FileNotFoundError, parsing.parse_contour_file("not_existing_file"))
        self.assertRaises(TypeError, parsing.parse_contour_file(None))


    def test_parse_dicom_file(self):
        """
        Unittest for parse_dicom_file() function
        tests for:
         - correct output data type 
         - correct error handling when file not existant
        """

        data_dir = "./data/dicoms/"

        for patient_dir in os.listdir(data_dir):
            for dicom in os.listdir(os.path.join(data_dir,patient_dir)):
                
                # TODO replace quickfix of repairing file string
                dicom = dicom.strip(".").strip("_")
                file_path = os.path.join(data_dir,patient_dir) + "/"+dicom

                # run function on dicom file
                output = parsing.parse_dicom_file(file_path)
                
                # test output format
                self.assertIsInstance(output, dict)
                self.assertIsInstance(output['pixel_data'], np.ndarray)


        # test error handling
        self.assertRaises(FileNotFoundError, parsing.parse_dicom_file("not_existing_file"))
        self.assertRaises(TypeError, parsing.parse_dicom_file(None))






def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def visualize_mask(mask):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(mask, aspect='auto', cmap=plt.cm.gray, interpolation='nearest')


