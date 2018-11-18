Preprocessing Pipeline for Medical Image Data

- before running, modify path_settings.py according to data folder structure 
- for unittests run python -m unittest 


Questions:

Part 1:

1. I implemented unittests to check for the expected output of the given functions. For parse_dicom and parse_contour I wrote independant testcases while I could only verify the polygon_to_mask function as part of the wrapper generate_input_target_arrays(). I also tested the validity of some masks by visualizing them in a matplotlib plot. It seemed to make sense, as I expected an inner contour to be a filled round shape, which differs in size across the slices. 

2. In the intial code there was an import of 'dicom' which I assumed to be referring to the pydicom module. In the first function there was no check for potentially
missing input files, so I added a try and except block. Additionally, I added more functions to wrap the given ones and map dicoms with their respective contour files. 


Part 2:

1. I built a data generator which handles the looping over the dataset and random sampling. In the first part, the pipeline only supplied the processed dataset as a whole.
As Keras uses these types of generators to feed data into their network, I built a similar data structure for further usage. I put it in a seperate class and wrapped Part 1 of generating the inputs and targets and Part 2 of creating a generator from the data in a function. This generator has a variable batch size, a fixed dataset size, which yields the amount of iterations it has to do for one epoch and samples the instances which are loaded per batch randomly. The indices for the chosen data samples are shuffled at the beginning and end of every epoch. 

2. I built unittests throughout development to incrementally built on working/tested functions. As I was already validating the creation of the inputs and targets in Part 1, I now focused on validating the generator. I tested the correct data types of the outputs and the variable batch size. It is rather hard to check the randomness of the generator and whether it covers every instance in one epoch as it has an infinite length and the only output is the data itself. I found a rather hacky solution by modifying the generator to output the indices of the data along with the arrays and checking the uniqueness of the indices per epoch in a hashtable. This validated, that each instance was outputted at least once. For the randomness criteria, I outputted the indices themselves to verify the randomness, but found, that the indices were not in a random order, despite calling np.random.shuffle() in the generator. Unfortunately, I found this bug too late and did not have enough time to fix it, but would in further steps suggest to 

3. Right now the pipeline first processes the entire dataset and then feeds it into the generator as a whole. That is problematic as the dataset size increases. I built in a function to store the data to disk after the first step which was not needed for a small dataset like this, but could be useful, when the dataset does not fit into memory anymore. Then I would have to make some adjustments to call the save_to_disk() function more often and adjust the generator to read the dataset from disk instead of passing it in as whole. A improvement would be to build the pipeline in real-time so that no data has to be stored. The preprocessing done in Part 1 would then be part integrated into the generator, which parses the dicoms and images as it calls the next batch of data. 