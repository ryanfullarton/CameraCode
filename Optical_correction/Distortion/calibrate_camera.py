import numpy as np
import sys
import cv2 as cv
import glob
import matplotlib.pyplot as plt

# termination criteria

def main(image_directory, rows, columns, square_size):
    """
        This function takes images of a chessboard pattern and generates a camera calibration GH_matrix
        The function uses the open CV library built in funtions for camera calibration

        The images should be at a variety of angles  distances from the camera to get a good calibration
    """
    #read in the image files
    images = glob.glob(image_directory + 'cal_image*.npy')
    #Set the interation end criteria [defaults]
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((columns*rows,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = objp * square_size # set the spacing of the object points

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    print(str(len(images)) + " images found")
    ret_num = 0
    for fname in images:
        img = np.uint8(np.load(fname))
        #show image
        cv.imshow('GrayImage',img)
        cv.waitKey(1000)
        cv.destroyAllWindows()
        # Find the chessboard corners
        ret, corners = cv.findChessboardCorners(img, (columns,rows), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(img,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv.drawChessboardCorners(img, (rows,columns), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(1000)
            ret_num+=1
    cv.destroyAllWindows()

    print(f"{ret_num} patterns matched")
    # Create the calibration matrix
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img.shape[::-1], None, None)
    print(mtx)
    # Save the calibration matrix
    np.save(image_directory + 'calibration_matrix.npy',mtx)
    # Save distortion coefficents
    np.save(image_directory + 'distortion_coefficients.npy', dist)

if len(sys.argv) < 5:
    print('Please enter the following arguments:\n'
    '1) Directory of image files\n'
    '2) Number of rows in the pattern\n'
    '3) Number of columns in the pattern\n'
    '4) Dimensions of a square side in the pattern\n')
main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
