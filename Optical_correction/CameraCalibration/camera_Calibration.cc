#include <opencv2/opencv.hpp>
#include <opencv2/calib3d/calib3d_c.h>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv_modules.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/core.hpp>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <sys/stat.h>




int main(int argc, char** argv)
{
  //arg1 - path to folder
  //arg2 - rows
  //arg2 - Columns
  //arg4 - Square dimensions
  // Defining the dimensions of checkerboard
  std::string arg2 = argv[2];
  std::cout<<arg2<<std::endl;
  int CHECKERBOARD[2]{std::stoi(arg2),std::atoi(argv[3])}; 
  std::cout<<CHECKERBOARD[0]<<" "<<CHECKERBOARD[1]<<std::endl;
  int square_edge = std::atoi(argv[4]);
  // Creating vector to store vectors of 3D points for each checkerboard image
  std::vector<std::vector<cv::Point3f> > objpoints;
  

  // Creating vector to store vectors of 2D points for each checkerboard image
  std::vector<std::vector<cv::Point2f> > imgpoints;

  // Defining the world coordinates for 3D points
  std::vector<cv::Point3f> objp;
  for(int i{0}; i<CHECKERBOARD[1]; i++)
  {
    for(int j{0}; j<CHECKERBOARD[0]; j++)
      objp.push_back(cv::Point3f(j*square_edge,i*square_edge,0));
  }


  // Extracting path of individual image stored in a given directory
  std::vector<cv::String> images;
  // Path of the folder containing checkerboard images
  std::string path = argv[1];
  cv::glob(path, images);

  cv::Mat frame, gray;
  // vector to store the pixel coordinates of detected checker board corners 
  std::vector<cv::Point2f> corner_pts;
  bool success;
  mkdir((path+"/calibrationData").c_str(),0777);
  // Looping over all the images in the directory
  for(int i{0}; i<images.size(); i++)
  {
    frame = cv::imread(images[i]);
    cv::cvtColor(frame,gray,cv::COLOR_BGR2GRAY);

    // Finding checker board corners
    // If desired number of corners are found in the image then success = true  
    success = cv::findChessboardCorners(gray, cv::Size(CHECKERBOARD[0], CHECKERBOARD[1]), corner_pts, CV_CALIB_CB_ADAPTIVE_THRESH | CV_CALIB_CB_FAST_CHECK | CV_CALIB_CB_NORMALIZE_IMAGE);
    
    /* 
     * If desired number of corner are detected,
     * we refine the pixel coordinates and display 
     * them on the images of checker board
    */
    if(success)
    {
      cv::TermCriteria criteria(CV_TERMCRIT_EPS | CV_TERMCRIT_ITER, 30, 0.001);
      
      // refining pixel coordinates for given 2d points.
      cv::cornerSubPix(gray,corner_pts,cv::Size(11,11), cv::Size(-1,-1),criteria);
      
      // Displaying the detected corner points on the checker board
      cv::drawChessboardCorners(frame, cv::Size(CHECKERBOARD[0], CHECKERBOARD[1]), corner_pts, success);
      
      objpoints.push_back(objp);
      imgpoints.push_back(corner_pts);
    }

    cv::imshow("Image",frame);
    cv::waitKey(500);
    cv::destroyAllWindows();
  }


  cv::Mat cameraMatrix,distCoeffs,R,T;

  /*
   * Performing camera calibration by 
   * passing the value of known 3D points (objpoints)
   * and corresponding pixel coordinates of the 
   * detected corners (imgpoints)
  */
  cv::calibrateCamera(objpoints, imgpoints, cv::Size(gray.rows,gray.cols), cameraMatrix, distCoeffs, R, T);

  std::cout << "cameraMatrix : " << cameraMatrix << std::endl;
  std::cout << "distCoeffs : " << distCoeffs << std::endl;
  std::cout << "Rotation vector : " << R << std::endl;
  std::cout << "Translation vector : " << T << std::endl;
  
  std::ofstream calfile;
  calfile.open (path +"/calibrationData/" + "calibrationMatrix.txt");
  calfile << cameraMatrix;
  calfile.close();

  std::ofstream distortionFile;
  distortionFile.open (path +"/calibrationData/" + "distortionCoefficients.txt");
  distortionFile << distCoeffs;
  distortionFile.close();

  std::ofstream RVecFile;
  RVecFile.open (path +"/calibrationData/" + "rotationVectors.txt");
  RVecFile << R;
  RVecFile.close();

  std::ofstream TVecFile;
  TVecFile.open (path +"/calibrationData/" + "translationVectors.txt");
  TVecFile << T;
  TVecFile.close();
}
