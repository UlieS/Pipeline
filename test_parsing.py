""" Unittests for parsing.py """

import unittest
import parsing 
import os 
import numpy as np
import pydicom
import path_settings as ps


class TestParsing(unittest.TestCase):

    def test_parse_contour_file(self):
        """
        Unittest for parse_contour_file() function
        tests for:
         - correct output data type 
         - output file includes all information from input file 
         - correct error handling when file not existant
        """

        # tests all available data on the function
        for patient_dir in os.listdir(ps.DATA_DIR_CONTOUR):
            file_path = os.path.join(ps.DATA_DIR_CONTOUR,patient_dir+ps.CONTOUR_TYPE)

            for contour in os.listdir(file_path):   
                # TODO replace quickfix for handling corrupt string
                contourfile = file_path+"/"+contour.strip("._")
              
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

        for patient_dir in os.listdir(ps.DATA_DIR_DICOM):
            for dicom in os.listdir(os.path.join(ps.DATA_DIR_DICOM,patient_dir)):
                
                # TODO replace quickfix of repairing file string
                dicom = dicom.strip(".").strip("_")
                file_path = os.path.join(ps.DATA_DIR_DICOM,patient_dir) + "/"+dicom

                # run function on dicom file
                output = parsing.parse_dicom_file(file_path)
                
                # test output format
                self.assertIsInstance(output, dict)
                self.assertIsInstance(output['pixel_data'], np.ndarray)
                self.assertEqual(output['pixel_data'].shape, (256,256))


        # test error handling
        self.assertRaises(FileNotFoundError, parsing.parse_dicom_file("not_existing_file"))
        self.assertRaises(TypeError, parsing.parse_dicom_file(None))


    def test_generate_input_target_arrays(self):
        """ function to verify the wrapper of all functions in parsing.py
            
            tests for:
            - correct input, target datatype and size
            - correct number of patients processed
        """
        output = parsing.generate_input_target_arrays(ps.LINKFILE)
        input, target = output

        self.assertIsInstance(input, np.ndarray)
        self.assertIsInstance(target, np.ndarray)

        # correct number of patients 
        patient_dicom_mapping = parsing.link_patient_contour_id(ps.LINKFILE)
        self.assertEqual(len(patient_dicom_mapping),5)

        # test equal length of input and target
        self.assertEqual(input.shape[0], target.shape[0])
       
        # test equal shape of arrays in target and input
        # only makes sense if previous test ran ok
        for i in range(input.shape[0]):
            self.assertEqual(input[i].shape, target[i].shape)
        



def file_length(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1



