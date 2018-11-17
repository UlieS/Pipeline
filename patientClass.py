import os

data_dir = "./data/dicoms/"
contour_type = "/i-contours"
data_dir_con = "./data/contourfiles/" 

class Patient:
    """  Patient class to organize files

        initialized with:
        :param patient_id: string 
        :param original_id: string 
    """
    def __init__(self, patient_id, original_id):
        self.patient_id = patient_id
        self.original_id = original_id
        self.dicom_path = data_dir+patient_id
        self.contour_path = data_dir_con+original_id+contour_type


    def map_dicom_contour(self):
        """ function to map pairs of dicom and contourfile

        checks in both directions for available mapping (contour -> dicom, dicom -> contour)
        :returns: dict object containing mapping of dicom and contourfile on patient level
        """
        dicom_contour_mapping = {}
        dicom_list = {}

        # create dictionary of dicoms for fast checking of existance
        for dicom in os.listdir(self.dicom_path):
            dicom_list[dicom.split(".")[0]]= dicom           

        # loops over all contours to find every match (contour -> dicom)
        for contour in os.listdir(self.contour_path):  
            num = int(contour.split("-")[2])

            # will succeed only if matching dicom is found in dict (dicom -> contour)
            try: 
                dicom = dicom_list[str(num)]
            except: 
                pass
            else: 
                dicom_contour_mapping[dicom] = contour
        
        return dicom_contour_mapping
