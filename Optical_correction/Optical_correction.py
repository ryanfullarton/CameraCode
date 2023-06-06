import numpy as np
import cv2 as cv 
import glob
import sys
import os
import cv2 as cv
from undistort_image import undistort_function
from vignetting_correction import vingetting_correction
#from projection_correction import projection_correction
#from refraction_correction import refraction_correction


def main(image_folder, format, calibration_matrix, distortion_coefficients):
    
    corrected_image_path = image_folder + 'optical_corrected/'
    try:
        os.mkdir(corrected_image_path)
    except FileExistsError:
        pass

    image_files = glob.glob(image_folder + '*' + format)
    for file in image_files:
        image = cv.imread(file) #np.load(file)
        image = np.array(image,dtype=np.uint16)
        filename = file.split('/')[-1][:-len(format)]
        #image = projection_correction(image)
        #image = refraction_correction(image)
        image = vingetting_correction(image, calibration_matrix)
        image = undistort_function(image, calibration_matrix, distortion_coefficients,1)
        np.save(corrected_image_path + filename, image)


if len(sys.argv) < 5 or len(sys.argv) > 5:
    print("Please enter the following arguments: \n"
    "1) Folder containing the image_names \n"
    "2) Format (extension) of images requiring correction \n"
    "3) Camera calibration matrix (npy file)\n"
    "4) Camera calibration distortion coefficients (npy file)")
else:
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])