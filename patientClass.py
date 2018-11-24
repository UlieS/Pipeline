import os
import path_settings as ps

class Patient:
    """  Patient class to organize files

        initialized with:
        :param patient_id: string 
        :param original_id: string 
    """
    def __init__(self, patient_id, original_id):
        self.patient_id = patient_id
        self.original_id = original_id
        self.dicom_path = ps.DATA_DIR_DICOM+patient_id
        self.icontour_path = ps.DATA_DIR_CONTOUR+original_id+"/i-contours"
        self.ocontour_path = ps.DATA_DIR_CONTOUR+original_id+"/o-contours"

    def map_dicom_contour(self, type):
        """ function to map pairs of dicom and i-contourfile
        checks in both directions for available mapping (contour -> dicom, dicom -> contour)
        
        :param type: string, type of contour to be parsed, choices: 'i', 'o'
        :returns: dict object containing mapping of dicom and contourfile on patient level
        """
        dicom_contour_mapping = {}
        dicom_list = {}

        # create dictionary of dicoms for fast checking of existance
        for dicom in os.listdir(self.dicom_path):
            dicom_list[dicom.split(".")[0]]= dicom           

        if type == "i":
            path = self.icontour_path
        elif type == "o":
            path = self.ocontour_path
        else:
            raise ValueError("Unknown contour-type '" + str(type) + "', choose 'i' or 'o'")

        # loops over all contours to find every match (contour -> dicom)
        for contour in os.listdir(path):  
            num = int(contour.split("-")[2])

            # will succeed only if matching dicom is found in dict (dicom -> contour)
            try: 
                dicom = dicom_list[str(num)]
            except: 
                pass
            else: 
                # tuple as item to be able to treat combined mapping in a similar way
                # as handling only o/i-contours
                dicom_contour_mapping[dicom] = (contour, "")
        
        return dicom_contour_mapping


    def combine_mappings(self, dicom_ocontour_mapping, dicom_icontour_mapping):
        """ computes the intersection of i and o contours given the respective dicom mappings
        
        :param dicom_ocontour_mapping: dictionary containing the mapping between o-contour and 
         dicom
        :param dicom_ocontour_mapping: dictionary containing the mapping between i-contour and 
         dicom
        :returns: intersected mapping of both contours
        """
        
        # generate intersection of the contours that are available for both types of contours 
        intersection = dicom_icontour_mapping.keys() & dicom_ocontour_mapping.keys()

        dicom_contour_mapping = {}
        
        # generate new combined mapping using the keys of the intersection 
        for key in intersection:
            dicom_contour_mapping[key] = (dicom_icontour_mapping[key][0], dicom_ocontour_mapping[key][0])

        return dicom_contour_mapping


    def dicom_contour_mapping_wrapper(self):
        """ wrapper function to execute parsing of both contour types and intersection
        
        :returns: intersected mapping of both contours    
        """

        icontour = self.map_dicom_contour("i")
        ocontour = self.map_dicom_contour("o")
        intersected_contour = self.combine_mappings(ocontour, icontour)

        return intersected_contour 


"""
p = Patient("SCD0000201","SC-HF-I-2")
i = p.dicom_contour_mapping_wrapper()
b = p.map_dicom_contour("i")
print("h")
"""