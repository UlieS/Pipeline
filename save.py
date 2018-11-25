import h5py


def save_data_to_disk(itarget, otarget, input, path='./data/processed_data.h5'):
    """ function to store target and input arrays on disk as h5py file

    :param itarget: np.array of icontour target data 
    :param otarget: np.array of ocontour target data
    :param input: np.array of input data 
    :param path: location of stored data, default in data folder
    """

    hf = h5py.File(path, 'w')
    hf.create_dataset('itarget', data=itarget)
    hf.create_dataset('otarget', data=otarget)
    hf.create_dataset('input', data=input)

    hf.close()


def read_data_from_disk(file='./data/processed_data.h5'):
    """ function to read data from h5py file
    
    :param file: path to stored h5py file
    :return: tuple of input and target arrays to be passed to generator
    """

    f = h5py.File(file)
    itarget = f['itarget'].value
    otarget = f['otarget'].value
    input = f['input'].value

    return input, itarget, otarget