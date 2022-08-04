# import required packages
import numpy as np
import sys
import cv2 as cv
import os

def main(calibration_matrix_file, image_path):
    #load calibration matrix
    calibration_matrix = np.load(calibration_matrix_file)

    #create focal length and center variables
    f_x = calibration_matrix[0,0]
    f_y = calibration_matrix[1,1]
    c_x = calibration_matrix[0,2]
    c_y = calibration_matrix[1,2]
    f = np.mean(np.asarray((f_x,f_y)))
    # set physical pixel size
    px_size = 0.0045

    #load image
    #im = np.load(image_path)
    image_directory = image_path.split('/')
    image_directory = image_directory[0:-1]
    image_directory = '/'.join(image_directory)
    image_directory = image_directory + '/Vingetting_corrected/'
    try:
        os.mkdir(image_directory)
    except FileExistsError:
        pass

    im = cv.imread(image_path)
    cv.imshow('GrayImage',im)
    cv.waitKey(5000)

    # loop over every pixel 
    for i in range(0,im.shape[0]):
        for j in range(0,im.shape[1]):
            #calculate distance from optical center
            dist_x = c_x - j
            dist_y = c_y - i
            dist_squared = (dist_x**2) + (dist_y**2)
            #calculate Vij
            V_numerator = f**4
            V_denominator = ((f**2)+dist_squared)**2 
            V = V_numerator/V_denominator
            # assign new pixel value 
            im[i,j] = im[i,j]/V

    cv.imshow('GrayImage',im)
    cv.waitKey(5000)
    # save new image
    np.save(image_directory + 'corrected.tiff',im)


main(sys.argv[1],sys.argv[2])