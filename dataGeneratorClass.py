import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    """ Data Generator class for handling looping over data 
        
         to note: for verifying uniqueness of the covered samples per batch 
         in unittest, comment in the additional inds return value 

    :param batchsize: int to determine batchsize
    :param input: np.array of input data
    :param target: np.array of target data 
    :return: instance of a data generator
    """

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
        input_batch = self.input[inds]
        target_batch = self.target[inds]
        
        # for verifying covering all instances return inds       
        # return input_batch, target_batch, inds
        
        return input_batch, target_batch
