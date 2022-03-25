import os
import PySpin as ps
import time
import json
import sys
import numpy as np



def set_settings(nodemap, config_parameters):
    """
        This function sets the camera acquisition parameters from the config file
        Each parameter requires retriving a node from the PySpin nodemap object
        then it retrieves the desired value for the parameter from the config file
        finally it sets the node to this value
        TODO: have the function output the resulting FPS not the set FPS of the camera
    """

    #Auto exposure on or off
    node_exposure_auto = ps.CEnumerationPtr(nodemap.GetNode('ExposureAuto'))
    entry_exposure_auto_off = node_exposure_auto.GetEntryByName(config_parameters['AUTO_EXPOSURE'])
    exposure_auto_off = entry_exposure_auto_off.GetValue()
    node_exposure_auto.SetIntValue(exposure_auto_off)

    # Exposure time only needed if auto exposure is off
    if config_parameters['AUTO_EXPOSURE'].lower() == 'off':
        node_exposure_time = ps.CFloatPtr(nodemap.GetNode('ExposureTime'))
        time_to_set = config_parameters['EXPOSURE']
        node_exposure_time.SetValue(time_to_set)

    # Auto gain on or off
    node_gain_auto = ps.CEnumerationPtr(nodemap.GetNode('GainAuto'))
    entry_gain_auto_off = node_gain_auto.GetEntryByName(config_parameters['AUTO_GAIN'])
    gain_auto_off = entry_gain_auto_off.GetValue()
    node_gain_auto.SetIntValue(gain_auto_off)

    # Gain value only required if auto gain is off
    if config_parameters['AUTO_GAIN'].lower() == 'off':
        node_gain = ps.CFloatPtr(nodemap.GetNode('Gain'))
        gain_to_set = config_parameters['GAIN']
        node_gain.SetValue(gain_to_set)

    #Pixel format - the bit depth of the acquired images
    node_pixel_format = ps.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
    node_pixel_format_mono8 = ps.CEnumEntryPtr(node_pixel_format.GetEntryByName(config_parameters['BIT_DEPTH']))
    node_pixel_format = node_pixel_format_mono8.GetValue()

    #Bit depth of the Analogue-digital converter
    node_pixel_ADC = ps.CEnumerationPtr(nodemap.GetNode('AdcBitDepth'))
    node_pixel_ADC_value = ps.CEnumEntryPtr(node_pixel_ADC.GetEntryByName(config_parameters['ADC_BIT_DEPTH']))
    node_pixel_ADC = node_pixel_ADC_value.GetValue()

    node_ISP = ps.CBooleanPtr(nodemap.GetNode('IspEnable'))
    ISP_to_set = config_parameters['ISP'].lower() == "true"
    node_ISP.SetValue(ISP_to_set)
    #Whether binning is to be achieved through averaging or summing
    bin_vert_mode = ps.CEnumerationPtr(nodemap.GetNode('BinningVerticalMode'))
    node_bin_vert_sum = ps.CEnumEntryPtr(bin_vert_mode.GetEntryByName(config_parameters['BIN_METHOD']))
    bin_vert_mode = node_bin_vert_sum.GetValue()

    bin_hoz_mode = ps.CEnumerationPtr(nodemap.GetNode('BinningHorizontalMode'))
    node_bin_hoz_sum = ps.CEnumEntryPtr(bin_hoz_mode.GetEntryByName(config_parameters['BIN_METHOD']))
    bin_hoz_mode = node_bin_hoz_sum.GetValue()

    #Number of bins per pixel (1-4)
    vert_binning = ps.CIntegerPtr(nodemap.GetNode('BinningVertical'))
    vert_binning_to_set = config_parameters['BINS']
    vert_binning.SetValue(vert_binning_to_set)

    hoz_binning = ps.CIntegerPtr(nodemap.GetNode('BinningHorizontal'))
    hoz_binning_to_set = config_parameters['BINS']
    hoz_binning.SetValue(hoz_binning_to_set)
    #for binning > 2 the ISP needs to be turned on so this parameter is redundant
    if config_parameters['BINS'] <3:
        node_ISP = ps.CBooleanPtr(nodemap.GetNode('IspEnable'))
        ISP_to_set = config_parameters['ISP'].lower() == "true"
        node_ISP.SetValue(ISP_to_set)

    #reset offset to avoid errors
    node_offsetx = ps.CIntegerPtr(nodemap.GetNode('OffsetX'))
    offsetx_to_set = 0
    node_offsetx.SetValue(offsetx_to_set)

    node_offsety = ps.CIntegerPtr(nodemap.GetNode('OffsetY'))
    offsety_to_set = 0
    node_offsety.SetValue(offsety_to_set)

    #Width of the acquired images in pixels
    node_width = ps.CIntegerPtr(nodemap.GetNode('Width'))
    width_to_set = config_parameters['WIDTH']
    node_width.SetValue(width_to_set)

    #Height of the acquired images in pixels
    node_height = ps.CIntegerPtr(nodemap.GetNode('Height'))
    height_to_set = config_parameters['HEIGHT']
    node_height.SetValue(height_to_set)

    # Image offset in the x direction
    node_offsetx = ps.CIntegerPtr(nodemap.GetNode('OffsetX'))
    offsetx_to_set = config_parameters['OFFSET_X']
    node_offsetx.SetValue(offsetx_to_set)

    # Image offset in the y direction
    node_offsety = ps.CIntegerPtr(nodemap.GetNode('OffsetY'))
    offsety_to_set = int(((600-config_parameters['HEIGHT'])/2)) + 219 #config_parameters['OFFSET_Y']
    node_offsety.SetValue(offsety_to_set)

    #Return the Frame rate of resulting from the acquisition parameters
    FPS = ps.CFloatPtr(nodemap.GetNode('AcquisitionFrameRate')).GetValue()
    return FPS


def main(output, config):
    """
        Main function that takes in the config file and output directory
        the funtion initialises the camera and handles the acquisition,
        and saving of the images acquired.

        TDOD : This function would work better as 5 separate funtions
            1) Initilise camera
            2) Trigger mode function
            3) Time mode function
            4) Continuous mode funtion
            5) Uninitialise camera
        TODO: Have the option to save frame by frame or with accumulated acquisition for all operating types
        TODO: Once the trigger is implemented add an external trigger mode
        TODO: Add a multi-camera mode e.g. acts on all cameras in the list not just one
    """
    #open the config file
    with open(config, "r") as f:
        config_parameters = json.load(f)

    #create empty list for the cameras
    camera_list = []
    #start an instance of the PySpin API
    system = ps.System.GetInstance()
    # Get list of connected cameras and enumerate them, adding to the camera list
    cam_list = system.GetCameras()
    for i, cam in enumerate(cam_list):
        camera_list.append(cam)

    #Define camera 1 as a camera object within the API and initilise it
    cam_1 = camera_list[0]
    cam_1.Init()

    #return the node map to set acquisition parameters
    nodemap = cam_1.GetNodeMap()
    #Set the acquisiton paraeters and return the frame rate (see above function)
    FPS = set_settings(nodemap, config_parameters)
    print(f"Frame Rate: {FPS}")

    #Set intialial booleans reqired for acquisition logic
    acquiring = True # is acquiring
    cam_1.BeginAcquisition() # start acquisition
    i=0 #begin acquisition count
    first = True # required for determining first frame of an acquisition
    triggered = False #Acquisition trigger for trigger mode off
    start = True # for printing when data is being acquired for trigger mode
    timeout = (int)(cam_1.ExposureTime.GetValue() / 1000 + 10) #determines time between retrieving frames from the camera
    threshold = 0. # Set threshold for trigger to zero
    b=0 # set counter for number of background images at 0
    image_result = cam.GetNextImage(timeout) #retrieve image from the camera after timeout
    image_data = image_result.GetNDArray() #retrieve the array of image data
    bg_arr = np.zeros(image_data.shape,dtype=np.float32) #set background array to match size of image array with value of 0
    t_end = time.time() + 10 # Set backqroung acquisition time (10s)
    while time.time()<t_end: # Acquire backgroun averaging over t_end
        image_result = cam.GetNextImage(timeout)
        image_data = image_result.GetNDArray()
        bg_arr += image_data #add image data to background array
        threshold += np.percentile(image_data, 100) # Set add percentile of pixel values to the threshold
        image_result.Release() # release image to acquire the next one
        b+=1 # increment counter to track number of images involved in background

    threshold = (2*threshold)/b # average threshold over all background images
    np.save(output + "Background" + ".npy", bg_arr/b) #save background array as a numpy .npy file
    print("Ready to acquire")

    t_test_end = time.time() + 10
    while acquiring: # will loop while acquiring is True
        if config_parameters['ACQUISITION_MODE'].lower() == 'trigger': # for acquisition mode trigger
            try: # This puts the whole process within a loop that ends after a keyboard interrupt (Ctrl + C)
                image_result = cam.GetNextImage(timeout) #get image
                image_data = image_result.GetNDArray() #return image array
                if first: #for first image set the acquisition array to the same size full of zeros
                    arr = np.zeros(image_data.shape)
                    first = False # no longer first acquisition
                    #print(np.percentile(image_data,99),threshold)
                if np.percentile(image_data,99) > threshold: #checks whether image data is above background levels (i.e. there is scintillation light)
                    triggered = True # Start acquiring
                while triggered:
                    if start: # This ensures this statement only prints once per acquisition
                        print("Acquiring data")
                    start = False
                    image_result = cam.GetNextImage(timeout) #Get image
                    image_data = image_result.GetNDArray() # retunr image array
                    arr = arr + image_data # add image array to acquisition array
                    if np.percentile(image_data,100) <= threshold: # checks if image data is below background (i.e. no scintillation light)
                        triggered =False # stop acuisition
                        first = True # reset for next acquisition
                        start = True # reset for next acuquisition
                        print("Acqiusition stopped")
                        np.save(output + "acquisition" + str(i) + ".npy", arr) # save as numpy .npy file
                        i+=1 #incremet the number of acquisitions for unique file names
                        print("image saved\n"
                             "Ready to acquire")
                    if triggered: # releases image to allow the next one if still triggered
                        image_result.Release()
                try: # trys to release the image to allow the next one if not triggered
                    image_result.Release()
                except:
                    pass
            except KeyboardInterrupt: # Stops acquisition session  when stop command entered (Ctrl + C)
                acquiring = False

        elif config_parameters['ACQUISITION_MODE'].lower() == 'time': # acqisition mode timed - Frame by frame mode
            acquisition_time = config_parameters['ACQUISITON_TIME'] # retrive acquisition time from config file
            t_stop = time.time() +  acquisition_time #sets the time at which the aquisition should end
            while time.time() < t_stop: # loops until the acquisition should end
                if start:
                    print("Acquiring data")
                start=False
                image_result = cam.GetNextImage(timeout) # Get image
                image_data = image_result.GetNDArray() # Return image array
                np.save(output + "frame" + str(i) + ".npy", image_data) # save image as numpy .npy file
                i+=1 # increment the acquisition counter for unique file names
                image_result.Release() # release image so the next one can be allowed to be read
            print("Acqiusition stopped")
            acquiring = False # Stops acquiring after the set time

        elif config_parameters['ACQUISITION_MODE'].lower() == 'continuous': # acquires until stop command (Ctrl + C)
            try: # Sets up ability to stop acquisition on stop command
                if start:
                    input()
                    print("Acquiring data")
                start=False
                image_result = cam.GetNextImage(timeout) # Get image
                image_data = image_result.GetNDArray() # Return image array
                np.save(output + "frame" + str(i) + ".npy", image_data) #save image as numpy .npy file
                i+=1 # increment acquisition counter for unique file names
                image_result.Release() # release image so the next one can be read
            except KeyboardInterrupt: # stops acquisition on the stop command (Ctrl + C)
                acquiring = False
                print("Acqiusition stopped")

        else: # Stops session when no valid acquisition mode is in the config file
            print("Invalid acquisition mode")
            acquiring = False

    print("\nEnd of session")

    # These commands disconnect the camera and end the PySpin connection removing residual data
    try:
        image_result.Release()
    except:
        pass
    cam_1.EndAcquisition()
    cam_1.DeInit()
    del cam
    del cam_1
    cam_list.Clear()
    camera_list.clear()
    system.ReleaseInstance()

#Checks the number of arguments entered is acceptable
if len(sys.argv) < 3:
    #provides argument information if this is not the case
    print('Please enter the following arguments:\n'
    '1) Path to the configuration file\n'
    '2) Path to output directory\n')
else: # runs main function
    main(sys.argv[2], sys.argv[1])
