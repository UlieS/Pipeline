import parsing
import save
from dataGeneratorClass import DataGenerator
import path_settings as ps


def pipe_data(batchsize, store_data_on_disk = False):
    """ main function for generating input and target data and 
     building generator

    :param batchsize: int to determine number of loaded observations 
     per batch in the generator
    :param store_data_on_disk: Bool to flag whether storing to disk is needed
    :return: data generator object to be used for training model
    """

    input, target = parsing.generate_input_target_arrays(ps.LINKFILE)
    
    # for larger datasets keep the option of storing data to disk
    if store_data_on_disk:
        save.save_data_to_disk(target,input)

    data_generator = DataGenerator(batchsize, input, target)
    
    return data_generator



