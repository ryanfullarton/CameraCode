import numpy as np
import cv2 as cv
import sys


def main(input_image_path, calibration_matrix, dist_coeffs, crop):
    #load in image as numpy array and convert to unsigned int for grayscale image
    img = np.load(input_image_path)
    img = np.uint8(img)
    #load in calibration matrix and distortion coefficients
    mtx = np.load(calibration_matrix)
    dist = np.load(dist_coeffs)

    #get shape of distorted image
    h,  w = img.shape[:2]

    # Funtion that opgtimises the camera calibration matrix based on the height of the image
    # The crop option [0] removes any black space created by undistorting
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), crop, (w,h))

    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    #save the image in the same folder
    np.save(input_image_path[:-4] + '_undistorted', dst)

if len(sys.argv) < 4:
    print('Please enter the following arguments:\n'
        '1) Path to distorted image\n'
        '2) Path to calibration matrix\n'
        '3) Path to distortion coefficients\n'
        '4) Whether to crop the undistorted image to remove black space [0 or 1]\n')


main(sys.argv[1], sys.argv[2],sys.argv[3], int(sys.argv[4]))
