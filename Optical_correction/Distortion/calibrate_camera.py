import numpy as np
import sys
import cv2 as cv
import glob
from PIL import Image
import matplotlib.pyplot as plt

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

rows = int(sys.argv[2])
columns = int(sys.argv[3])
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((columns*rows,3), np.float32)
objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob(sys.argv[1] + 'cal_image*.npy')
print(str(len(images)) + " images found")
ret_num = 0
for fname in images:
    img = np.uint8(np.load(fname))
    cv.imshow('GrayImage',img)
    cv.waitKey(1000)
    cv.destroyAllWindows()
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
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img.shape[::-1], None, None)
print(mtx)
np.save('./images/calibration_matrix.npy',mtx)
