import unittest
import parsing 
import os 
import numpy as np
import pipeline
import path_settings

class TestPipeline(unittest.TestCase):

    def test_pipe_data(self):
        datagen = pipeline.pipe_data(7)
        for batch in datagen:
            self.assertIsInstance(batch,tuple)
            
            input, target = batch
            self.assertEqual(target.shape[0], 7)
            self.assertEqual(input.shape[0], 7)
            self.assertIsInstance(input[0], np.ndarray)
            self.assertIsInstance(target[0], np.ndarray)
            self.assertEqual(input.shape[1], 256)
            self.assertEqual(target.shape[1], 256)


if __name__ == "__main__":
    unittest.main()