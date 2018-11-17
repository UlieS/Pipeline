import numpy as np


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
        inds = self.indices[idx:idx+self.batchsize]
        input_batch = self.input[inds]
        target_batch = self.target[inds]
        #input_batch = np.array(np.resize(input[inds], (self.batchsize,1,self.dim,self.dim,)))
        #target_batch =  np.array(np.resize(target[inds], (self.batchsize,1,self.dim,self.dim)))
        return input_batch, target_batch