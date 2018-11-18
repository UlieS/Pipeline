import unittest
import parsing
import pipeline
import path_settings as ps
import os 
import numpy as np


class TestPipeline(unittest.TestCase):
    """ function to test the main function pipe_data()

        - when using this, modify dataClassGenerator to output indices as well, otherwise 
        uniqueness check will fail 

        tests for:
        - correct output of generator 
        - correct batchsize
        - covering every sample
    """

    def test_pipe_data(self):
        dataset_size = 96
        batch_size = 8

        datagen = pipeline.pipe_data(batch_size)
        check_every_instance = {}   

        #  number of iterations per epoch 
        num_iter = int(np.floor(dataset_size / batch_size))

        count = 0
        for batch in datagen: 
            count += 1 

            input, target, inds = batch

            # check general output criteria only once
            if count == 2: 
                self.assertIsInstance(batch,tuple)
                self.assertEqual(target.shape[0], batch_size)
                self.assertEqual(input.shape[0], batch_size)
                self.assertIsInstance(input[0], np.ndarray)
                self.assertIsInstance(target[0], np.ndarray)
                self.assertEqual(input.shape[1], 256)
                self.assertEqual(target.shape[1], 256)

            

            for idx in inds: 
                check_every_instance[idx]= True
            
            # if dictionary has encountered each instance once, 
            # the dictionary should contain the same number of elements as the dataset 
            if count == num_iter:
                self.assertEqual(len(check_every_instance), dataset_size)
                check_every_instance = {}
            
            # number of epochs = 4, stop generator after this number
            if count == num_iter*4:
                break
    
            
