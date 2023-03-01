import os
import PySpin as ps
import time
import json
import sys
import numpy as np
from Basic_acquisition import set_settings, write_log_file
import matplotlib.pyplot as plt
import keyboard

def main(output, config_1, config_2):
    """
        Main function that takes in the config file and output directory
        the funtion initialises the camera and handles the acquisition,
        and displays the images acquired.
    """
    #open the config file
    with open(config_1, "r") as f1:
        config_parameters_1 = json.load(f1)
    
    try:
        os.mkdir(output + config_parameters_1["CAMERA_VIEW"])
    except FileExistsError:
        pass

    #create empty list for the cameras
    camera_list = []
    #start an instance of the PySpin API
    system = ps.System.GetInstance()
    # Get list of connected cameras and enumerate them, adding to the camera list
    cam_list = system.GetCameras()
    for i, cam in enumerate(cam_list):
        camera_list.append(cam)

    if len(camera_list) > 1:
        mode = 'multi'
        with open(config_2, "r") as f2:
            config_parameters_2 = json.load(f2)
            try:
                os.mkdir(output + config_parameters_2["CAMERA_VIEW"])
            except FileExistsError:
                pass
    else:
        mode = 'single'

    for camera in camera_list:
        camera.Init()
        temp_nodemap = camera.GetNodeMap()
        camera_SN = ps.CStringPtr(temp_nodemap.GetNode('DeviceSerialNumber')).GetValue()
        
        camera.DeInit()
        if camera_SN == config_parameters_1['SERIAL_NUMBER']:
            #Define camera 1 as a camera object within the API and initilise it
            cam_1 = camera
            cam_1.Init()
            #return the node map to set acquisition parameters
            nodemap_1 = cam_1.GetNodeMap()
            cam_1_SN = camera_SN

        if mode == 'multi':
            if camera_SN == config_parameters_2['SERIAL_NUMBER']:
                #Define camera 1 as a camera object within the API and initilise it
                cam_2 = camera
                cam_2.Init()

                #return the node map to set acquisition parameters
                nodemap_2 = cam_2.GetNodeMap()
                cam_2_SN = camera_SN

    #Set the acquisiton paraeters and return the frame rate (see above function)
    
    FPS_aq_1, FPS_res_1 = set_settings(nodemap_1, config_parameters_1, output)
    
    if mode == 'multi':
        FPS_aq_2, FPS_res_2 = set_settings(nodemap_2, config_parameters_2, output)
        if FPS_res_2 > FPS_res_1:

            node_frame_rate_enable = ps.CBooleanPtr(nodemap_2.GetNode('AcquisitionFrameRateEnable'))
            frame_rate_enable = True
            node_frame_rate_enable.SetValue(frame_rate_enable)

            FPS_node = ps.CFloatPtr(nodemap_2.GetNode('AcquisitionFrameRate'))
            FPS_node.SetValue(FPS_res_1)

            FPS_res_2 = ps.CFloatPtr(nodemap_2.GetNode('AcquisitionResultingFrameRate')).GetValue()

        elif FPS_res_1 > FPS_res_2:

            node_frame_rate_enable = ps.CBooleanPtr(nodemap_1.GetNode('AcquisitionFrameRateEnable'))
            frame_rate_enable = True
            node_frame_rate_enable.SetValue(frame_rate_enable)

            FPS_node = ps.CFloatPtr(nodemap_1.GetNode('AcquisitionFrameRate'))
            FPS_node.SetValue(FPS_res_2)

            FPS_res_1 = ps.CFloatPtr(nodemap_1.GetNode('AcquisitionResultingFrameRate')).GetValue()


    print(f'Camera 1 ({cam_1_SN}):')
    print(f"Acquisition Frame Rate: {round(FPS_aq_1,0)}   Resulting Frame Rate: {round(FPS_res_1,0)}")
    if mode == 'multi':
        print(f'Camera 2 ({cam_2_SN}):')
        print(f"Acquisition Frame Rate: {round(FPS_aq_2,0)}   Resulting Frame Rate: {round(FPS_res_2,0)}")

    cam_1.BeginAcquisition() # start acquisition
    if mode == 'multi':
        cam_2.BeginAcquisition()

    if config_parameters_1["ACQUISITION_MODE"].lower() == 'external':
        timeout = (int) ((1./FPS_res_1) + 60000)
    else:
        timeout = (int)(cam_1.ExposureTime.GetValue() / 1000 + 60000) #determines time between retrieving frames from the camera
    if (1./FPS_res_1) + 10 > timeout:
        #print(timeout)
        timeout = (int) ((1./FPS_res_1) +60000) # for most cases exposure is the better time to use. This avoids errors trying to get images faster than the FPS
        #print(timeout)
    

    if mode == 'multi':
        fig, ax = plt.subplots(1,2)             
    else:
        fig, ax = plt.subplots(1) 
    # Close the GUI when close event happens
    recording = True

    while recording:
            
        image_result_1 = cam_1.GetNextImage(timeout)
        if mode == 'multi':
            image_result_2 = cam_2.GetNextImage(timeout)

        # Getting the image data as a numpy array
        image_data_1 = image_result_1.GetNDArray()
        if mode == 'multi':
            image_data_2 = image_result_2.GetNDArray()
        # Draws an image on the current figure
        ax[0].imshow(image_data_1, cmap='gray')
        if mode == 'multi':
            ax[1].imshow(image_data_2, cmap='gray')
        
        plt.show()
        # Interval in plt.pause(interval) determines how fast the images are displayed in a GUI
        # Interval is in seconds.
        plt.pause(0.001)

        # Clear current reference of a figure. This will improve display speed significantly
        plt.clf()
        
        # If user presses enter, close the program
        if keyboard.is_pressed('ENTER'):
            print('Program is closing...')
            
            # Close figure
            plt.close('all')             
            recording = False
    
    try:
        image_result_1.Release()
        if mode == 'multi':
            try:
                image_result_2.Release()
            except:
                pass
    except:
        if mode == 'multi':
            try:
                image_result_2.Release()
            except:
                pass

            
    cam_1.EndAcquisition()
    if mode == 'multi':
        cam_2.EndAcquisition()
    cam_1.DeInit()
    camera.DeInit()
    if mode == 'multi':
        cam_2.DeInit()
    del cam
    del cam_1
    del camera
    if mode == 'multi':
        del cam_2
    cam_list.Clear()
    camera_list.clear()
    system.ReleaseInstance()

