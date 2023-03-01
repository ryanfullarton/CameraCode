import numpy as np #This is a package that allows python to deal with arrays (matrices) efficently - The most useful python package in my opninion!
import sys #This package allows the code to interact with the system it's running on
import cv2 as cv #This is the openCV computer vision package
import glob # This is a directory pathway reader
import matplotlib.pyplot as plt # This package allows graph plotting and image display
import os # This allows the interaction of the operating system and the program


def main(image_directory, rows, columns, square_size):
    """
        This function takes images of a chessboard pattern and generates a camera calibration GH_matrix
        The function uses the open CV library built in funtions for camera calibration

        The images should be at a variety of angles  distances from the camera to get a good calibration


    """
    #read in the image files to a list
    images = glob.glob(image_directory + '*')
    #Set the interation end criteria [defaults]
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 500, 0.00001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) (chessbaord coordinates)
    objp = np.zeros((columns*rows,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = objp * square_size # set the spacing of the object points

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    # Ignore this next section!
    ChAruco = 'no'
    if ChAruco == 'yes':
        dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_250)
        board = cv.aruco.CharucoBoard_create(15, 8,0.005,0.004,dictionary)
        img = board.draw((50*15,50*8))
        #Dump the calibration board to a file
        cv.imwrite('charuco.png',img)

    # print the length of the list of image files
    print(str(len(images)) + " images found")
    
    ret_num = 0 # this sets a counter for how many images are successfully matched to a chessboard pattern

    for fname in images: # Loop over all files in the list
        print(fname) # output file name for user to see
        #img = np.uint8(np.load(fname)) # For use when working with npy files rather than .tiff images
        img = cv.imread(fname) # Read in the files into an image object
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # Chage the image to greyscale because the calibration works only on greyscale images
        
        cv.imshow('GrayImage',img) # Display image
        cv.waitKey(1000) # Wait a second
        cv.destroyAllWindows() # Close the window
        # Find the chessboard corners
        ret, corners = cv.findChessboardCorners(img, (columns,rows), None)
        # If found, add object points, image points (after refining them) to another list for storage
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(img,corners, (11,11), (-1,-1), criteria) #finds the sub-pixel corner positions
            imgpoints.append(corners2) 
            # Draw and display the corners
            cv.drawChessboardCorners(img, (rows,columns), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(5000)
            ret_num+=1
    ### This is the end of the loop through files
    cv.destroyAllWindows() # close all windows

    print(f"{ret_num} patterns matched") # Return how many patterns were successfully matched
    # Create the calibration matrix
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img.shape[::-1], None, None) #open CV function that uses the stored object and image points from all images
    #print(mtx)
    save_path = image_directory + "calibration_data/" # create a file path to save data into
    os.mkdir(save_path)  # make the above named file path
    # Save the calibration matrix
    np.save(save_path + 'calibration_matrix.npy',mtx) # save calibration matrix
    # Save distortion coefficents
    np.save(save_path + 'distortion_coefficients.npy', dist) # Save distortion coefficients 
    np.save(save_path + 'object_points.npy', objpoints) # Save object points
    np.save(save_path + 'image_points.npy', imgpoints) # Save image points
    np.save(save_path + 'tangential_vectors.npy', tvecs) # Save tangential distortion vectors
    np.save(save_path + 'radial_vectors.npy', rvecs) # Save radial distortion vectors

    mean_error_corrected = 0
    mean_error_uncorrected = 0
    for i in range(len(objpoints)): # loop over all sets of points (equal to the number of successfully matched images)
        uncorrected_projection, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist*0) # Project points with zero distortion correction
        error_uncorrected = cv.norm(imgpoints[i], uncorrected_projection, cv.NORM_L2)/len(uncorrected_projection) # calculate the error in the original image
        mean_error_uncorrected += error_uncorrected # add to the rolling mean (accross all images)
        #print('***************************************************************************')
        #print(objpoints[i])
        #print('***************************************************************************')
        #print(uncorrected_projection)
        #print('***************************************************************************')
        #print(imgpoints[i])
        projected_points, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist) # project the points with the distortion correction
        error_corrected = cv.norm(imgpoints[i], projected_points, cv.NORM_L2)/len(projected_points) #calcualte the image error between the corrected image and object points
        mean_error_corrected += error_corrected #add to the rolling mean (across all images)
        #print('***************************************************************************')
        #print(projected_points)

        print(f"Uncorrected error, image {i}: {error_uncorrected}") #display error in the original images (distortion)
        print(f"Corrected error, image {i}: {error_corrected}") # display how much distortion remains after reprojection with the cal matrix

    print( "Total uncorrected error: {}".format(mean_error_uncorrected/len(objpoints))) # display mean error for the user
    print( "Total corrected error: {}".format(mean_error_corrected/len(objpoints)))



#### IT ACTUALLY STARTS HERE ###

if len(sys.argv) < 5: # If you don't give it all the inforation it needs then it will not run but will tell you what it needs
    print('Please enter the following arguments:\n'
    '1) Directory of image files\n'
    '2) Number of rows in the pattern\n'
    '3) Number of columns in the pattern\n'
    '4) Dimensions of a square side in the pattern\n')
else: # run the main function above
    main(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
