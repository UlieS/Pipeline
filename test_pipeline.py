import unittest
import parsing 
import os 
import numpy as np
import pipeline


class TestPipeline(unittest.TestCase):

    def test_pipe(self):
        """

        """
        output = pipeline.pipe("./data/link.csv")
        input, target = output

        self.assertIsInstance(input, np.ndarray)
        self.assertIsInstance(target, np.ndarray)

        # test equal length of input and target
        self.assertEqual(input.shape[0], target.shape[0])
       
        # test equal shape of arrays in target and input
        # only makes sense if previous test ran ok
        for i in range(input.shape[0]):
            self.assertEqual(input[i].shape, target[i].shape)