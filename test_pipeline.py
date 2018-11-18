import unittest
import parsing 
import os 
import numpy as np
import pipeline
import path_settings

class TestPipeline(unittest.TestCase):
    """ function to test the main function pipe_data()
        tests for:
        - correct output of generator 
        - 
    """

    def test_pipe_data(self):
        datagen = pipeline.pipe_data(8)
        #print(list(datagen))
        for batch in datagen: 

            self.assertIsInstance(batch,tuple)
            
            input, target = batch
            print(target.shape[0])
            self.assertEqual(target.shape[0], 8)
            self.assertEqual(input.shape[0], 8)
            self.assertIsInstance(input[0], np.ndarray)
            self.assertIsInstance(target[0], np.ndarray)
            self.assertEqual(input.shape[1], 256)
            self.assertEqual(target.shape[1], 256)
            break
    
        #self.assertEqual(count, 1)

if __name__ == "__main__":
    unittest.main()