import os
import PySpin as ps
import time
import json
import sys
import numpy as np

def write_log_file(nodemap, config_parameters,SN, output):
    """ This function reads the current settings in the nodemap and writes them to a logfile in the output directory
        Can be used for debugging the set_settings function or acquisition record keeping
    """
    with open(output + config_parameters["CAMERA_VIEW"] + "/" + f'{SN}_parameters.txt', 'w') as log:
        FPS_aq = ps.CFloatPtr(nodemap.GetNode('AcquisitionFrameRate')).GetValue()
        FPS_res = ps.CFloatPtr(nodemap.GetNode('AcquisitionResultingFrameRate')).GetValue()
        SN = ps.CStringPtr(nodemap.GetNode('DeviceSerialNumber')).GetValue()
        exposure_mode = ps.CEnumerationPtr(nodemap.GetNode('ExposureMode')).GetCurrentEntry().GetDisplayName()
        trigger_source = ps.CEnumerationPtr(nodemap.GetNode('TriggerSource')).GetCurrentEntry().GetDisplayName()
        if config_parameters['ACQUISITION_MODE'].lower() == 'external':
            trigger_activation = ps.CEnumerationPtr(nodemap.GetNode('TriggerActivation')).GetCurrentEntry().GetDisplayName()
        #trigger_overlap = ps.CEnumerationPtr(nodemap.GetNode('TriggerOverlap')).GetCurrentEntry().GetDisplayName()
        trigger_delay = ps.CFloatPtr(nodemap.GetNode('TriggerDelay')).GetValue()
        shutter_mode = ps.CEnumerationPtr(nodemap.GetNode('SensorShutterMode')).GetCurrentEntry().GetDisplayName()
        gain_selector = ps.CEnumerationPtr(nodemap.GetNode('GainSelector')).GetCurrentEntry().GetDisplayName()
        
        auto_exposure = ps.CEnumerationPtr(nodemap.GetNode('ExposureAuto')).GetCurrentEntry().GetDisplayName()
        auto_gain = ps.CEnumerationPtr(nodemap.GetNode('GainAuto')).GetCurrentEntry().GetDisplayName()
        black_level_selecor = ps.CEnumerationPtr(nodemap.GetNode('BlackLevelSelector')).GetCurrentEntry().GetDisplayName()
        black_level = ps.CFloatPtr(nodemap.GetNode('BlackLevel')).GetValue()
        black_level_clamping = ps.CBooleanPtr(nodemap.GetNode('BlackLevelClampingEnable')).GetValue()
        pixel_format = ps.CEnumerationPtr(nodemap.GetNode('PixelFormat')).GetCurrentEntry().GetDisplayName()
        pixel_ADC = ps.CEnumerationPtr(nodemap.GetNode('AdcBitDepth')).GetCurrentEntry().GetDisplayName()
        gamma_enable = ps.CBooleanPtr(nodemap.GetNode('GammaEnable')).GetValue()
        sharpening_enable = ps.CBooleanPtr(nodemap.GetNode('SharpeningEnable')).GetDisplayName()
        ISP = ps.CBooleanPtr(nodemap.GetNode('IspEnable')).GetValue()
        binning_selector = ps.CEnumerationPtr(nodemap.GetNode('BinningSelector')).GetCurrentEntry().GetDisplayName()
        bin_mode = ps.CEnumerationPtr(nodemap.GetNode('BinningVerticalMode')).GetCurrentEntry().GetDisplayName()
        bin_vert = ps.CIntegerPtr(nodemap.GetNode('BinningVertical')).GetValue()
        bin_hoz = ps.CIntegerPtr(nodemap.GetNode('BinningHorizontal')).GetValue()
        width = ps.CIntegerPtr(nodemap.GetNode('Width')).GetValue()
        height = ps.CIntegerPtr(nodemap.GetNode('Height')).GetValue()
        offset_x = ps.CIntegerPtr(nodemap.GetNode('OffsetX')).GetValue()
        offset_y = ps.CIntegerPtr(nodemap.GetNode('OffsetY')).GetValue()
        decimation_selector = ps.CEnumerationPtr(nodemap.GetNode('DecimationSelector')).GetCurrentEntry().GetDisplayName()
        decimation_method = ps.CEnumerationPtr(nodemap.GetNode('DecimationHorizontalMode')).GetCurrentEntry().GetDisplayName()
        hoz_decimation = ps.CIntegerPtr(nodemap.GetNode('DecimationHorizontal')).GetValue()
        vert_decimation = ps.CIntegerPtr(nodemap.GetNode('DecimationHorizontal')).GetValue()

        t = time.localtime()
        log.write('Acquisition Time: ')
        log.write(time.strftime("%H:%M:%S", t) +' \n')
        log.write(f'Serial Number: {SN} \n')
        log.write(f"Camera View: {config_parameters['CAMERA_VIEW']} \n")
        log.write(f"Acquisition Mode: {config_parameters['ACQUISITION_MODE']} \n")
        if config_parameters['ACQUISITION_MODE'].lower() == 'time':
            log.write(f"Acquisition Time: {config_parameters['ACQUISITON_TIME']} \n")
        log.write(f'Exposure Mode: {exposure_mode} \n \n')
        if exposure_mode == 'Timed':
            log.write(f'Auto Exposure: {auto_exposure} \n')
            if auto_exposure != True:
                exposure_time = ps.CFloatPtr(nodemap.GetNode('ExposureTime')).GetValue()
                log.write(f'Exposure Time: {exposure_time} \n \n')

        log.write(f'Shutter Mode: {shutter_mode} \n \n')
        if config_parameters['ACQUISITION_MODE'].lower() == 'external':    
            log.write(f'Trigger Source: {trigger_source} \n')
            log.write(f'Trigger Activation: {trigger_activation} \n')
            #log.write(f'Trigger Overlap: {trigger_overlap} \n')
            log.write(f'Trigger Delay: {trigger_delay} \n \n')

        log.write(f'Gain Selector: {gain_selector} \n')
        log.write(f'Auto Gain: {auto_gain} \n')
        if auto_gain.lower() == 'off':
            gain = ps.CFloatPtr(nodemap.GetNode('Gain')).GetValue()
            log.write(f'Gain: {gain} \n')
        log.write('\n')

        log.write(f'Gamma Enable: {gamma_enable} \n')
        if gamma_enable == True:
            gamma = ps.CFloatPtr(nodemap.GetNode('Gamma')).GetValue()
            log.write(f'Gamma: {gamma} \n')
        log.write('\n')

        log.write(f'Sharpening Enabled: {sharpening_enable} \n')
        if sharpening_enable == True:
            sharpening_auto = ps.CBooleanPtr(nodemap.GetNode('SharpeningAuto')).GetValue()
            log.write(f'Auto Sharpening: {sharpening_auto} \n')
            if sharpening_auto == True:
                sharpening = ps.CIntegerPtr(nodemap.GetNode('Sharpening')).GetValue()
                log.write(f'Sharpening: {sharpening} \n')
        log.write('\n')

        log.write(f'Black Level Selector: {black_level_selecor} \n')
        log.write(f'Black Level Clamping: {black_level_clamping} \n')
        log.write(f'Black Level: {black_level} \n')
        log.write('\n')

        log.write(f'Pixel Format: {pixel_format} \n')
        log.write(f'Pixel ADC: {pixel_ADC} \n')
        log.write('\n')

        log.write(f'ISP: {ISP} \n')
        log.write('\n)')

        log.write(f'Bin Selector: {binning_selector} \n')
        log.write(f'Bin Mode: {bin_mode} \n')
        log.write(f'Vertical Binning: {bin_vert} \n')
        log.write(f'Horizontal Binning {bin_vert} \n')
        log.write('\n')

        log.write(f'Decimation Selector: {decimation_selector} \n')
        log.write(f'Decimation Mode: {decimation_method} \n')
        log.write(f'Horizontal Decimation: {hoz_decimation} \n')
        log.write(f'Vertical Decimation: {vert_decimation} \n')
        log.write('\n')

        log.write(f'Width: {width} \n')
        log.write(f'Height: {height} \n')
        log.write(f'Offset X: {offset_x} \n')
        log.write(f'Offset Y: {offset_y} \n')
        log.write('\n')

        log.write(f'Acquisition FPS: {FPS_aq} \n')
        log.write(f'Resulting FPS: {FPS_res} \n')
        log.close()
        print('Log file saved')


def set_settings(nodemap, config_parameters,output):
    """
        This function sets the camera acquisition parameters from the config file
        Each parameter requires retriving a node from the PySpin nodemap object
        then it retrieves the desired value for the parameter from the config file
        finally it sets the node to this value

        The funtion produces a text files with the settings from the camera before acquisition

        TODO: investigate bit depth and ADC because I don't think it's setting correctly*
        TODO: Debug sharpening and except for non-write errors
    """

    node_exposure_mode = ps.CEnumerationPtr(nodemap.GetNode('ExposureMode'))
    exposure_mode_set = node_exposure_mode.GetEntryByName(config_parameters['EXPOSURE_MODE'])
    node_exposure_mode.SetIntValue(exposure_mode_set.GetValue())

    
    #Trigger input - usually Line 5
    node_trigger_source = ps.CEnumerationPtr(nodemap.GetNode('TriggerSource'))
    node_trigger_source_value = node_trigger_source.GetEntryByName(config_parameters['TRIGGER_SOURCE'])
    node_trigger_source.SetIntValue(node_trigger_source_value.GetValue())

    #Trigger overlap TODO - find out exactly what this means??
    node_trigger_overlap = ps.CEnumerationPtr(nodemap.GetNode('TriggerOverlap'))
    node_trigger_overlap_value =node_trigger_overlap.GetEntryByName(config_parameters['TRIGGER_OVERLAP'])
    #node_trigger_overlap.SetIntValue(node_trigger_overlap_value.GetValue())

    # Trigger delay - time after trigger activation to start acquisition (microseconds)
    node_trigger_delay = ps.CFloatPtr(nodemap.GetNode('TriggerDelay'))
    node_trigger_delay_value = config_parameters['TRIGGER_DELAY']
    node_trigger_delay.SetValue(node_trigger_delay_value)

    node_trigger_mode = ps.CEnumerationPtr(nodemap.GetNode('TriggerMode'))
    if config_parameters['ACQUISITION_MODE'].lower() == 'external':
        trigger_mode_set = node_trigger_mode.GetEntryByName('On')
        #node_trigger_mode.SetIntValue(trigger_mode_set.GetValue())
            
        #Trigger activation point
        node_trigger_activation = ps.CEnumerationPtr(nodemap.GetNode('TriggerActivation'))
        node_trigger_activation_value = node_trigger_activation.GetEntryByName(config_parameters['TRIGGER_ACTIVATION'])
        node_trigger_activation.SetIntValue(node_trigger_activation_value.GetValue())

        node_line_selector = ps.CEnumerationPtr(nodemap.GetNode('LineSelector'))
        line_selector_trigger = node_line_selector.GetEntryByName('Line5')
        node_line_selector.SetIntValue(line_selector_trigger.GetValue())

        node_line_input = ps.CEnumerationPtr(nodemap.GetNode('LineMode'))
        line_input = node_line_input.GetEntryByName('Input')
        node_line_input.SetIntValue(line_input.GetValue())
    else:
        trigger_mode_set = node_trigger_mode.GetEntryByName('Off')
#        node_trigger_mode.SetIntValue(trigger_mode_set.GetValue())
    

    node_shutter_mode = ps.CEnumerationPtr(nodemap.GetNode('SensorShutterMode'))
    node_shutter_mode_value = node_shutter_mode.GetEntryByName(config_parameters['SHUTTER_MODE'])
    node_shutter_mode.SetIntValue(node_shutter_mode_value.GetValue())

    node_gain_selector = ps.CEnumerationPtr(nodemap.GetNode('GainSelector'))
    node_gain_selector_value = node_gain_selector.GetEntryByName(config_parameters['GAIN_SELECTOR'])
    node_gain_selector.SetIntValue(node_gain_selector_value.GetValue())

    #Auto exposure on or off
    node_exposure_auto = ps.CEnumerationPtr(nodemap.GetNode('ExposureAuto'))
    entry_exposure_auto_off = node_exposure_auto.GetEntryByName(config_parameters['AUTO_EXPOSURE'])
    exposure_auto_off = entry_exposure_auto_off.GetValue()
    node_exposure_auto.SetIntValue(exposure_auto_off)

    # Exposure time only needed if auto exposure is off
    if config_parameters['AUTO_EXPOSURE'].lower() == 'off' and config_parameters["EXPOSURE_MODE"] != 'TriggerWidth':
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

    node_black_level_selector = ps.CEnumerationPtr(nodemap.GetNode('BlackLevelSelector'))
    black_level_selector_to_set = node_black_level_selector.GetEntryByName(config_parameters['BLACK_LEVEL_SELECTOR'])
    black_level_selector_value = black_level_selector_to_set.GetValue()
    node_black_level_selector.SetIntValue(black_level_selector_value)

    node_black_level = ps.CFloatPtr(nodemap.GetNode('BlackLevel'))
    black_level_to_set = config_parameters['BLACK_LEVEL']
    node_black_level.SetValue(black_level_to_set)

    node_black_level_clamping = ps.CBooleanPtr(nodemap.GetNode('BlackLevelClampingEnable'))
    black_level_clamping_value = config_parameters['BLACK_LEVEL_CLAMPING'].lower() == 'true'
    node_black_level_clamping.SetValue(black_level_clamping_value)

    #Pixel format - the bit depth of the acquired images
    node_pixel_format = ps.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
    node_pixel_format_mono8 = ps.CEnumEntryPtr(node_pixel_format.GetEntryByName(config_parameters['BIT_DEPTH']))
    node_pixel_format.SetIntValue(node_pixel_format_mono8.GetValue())

    #Bit depth of the Analogue-digital converter
    node_pixel_ADC = ps.CEnumerationPtr(nodemap.GetNode('AdcBitDepth'))
    node_pixel_ADC_value = ps.CEnumEntryPtr(node_pixel_ADC.GetEntryByName(config_parameters['ADC_BIT_DEPTH']))
    node_pixel_ADC.SetIntValue(node_pixel_ADC_value.GetValue())

    node_gamma_enable = ps.CBooleanPtr(nodemap.GetNode('GammaEnable'))
    gamma_enable_value = config_parameters['GAMMA_ENABLE'].lower() == 'true'
    node_gamma_enable.SetValue(gamma_enable_value)

    if gamma_enable_value == True:
        node_gamma = ps.CFloatPtr(nodemap.GetNode('Gamma'))
        gamma_to_set = config_parameters['GAMMA']
        node_gamma.SetValue(gamma_to_set)
    try:
        node_sharpening_enable = ps.CBooleanPtr(nodemap.GetNode('SharpeningEnable'))
        sharpening_enable_value = config_parameters['SHARPENING_ENABLE'].lower() == 'true'
        node_sharpening_enable.SetValue(sharpening_enable_value)

        if sharpening_enable_value == True:
            node_auto_sharpen = ps.CBooleanPtr(nodemap.GetNode('SharpeningAuto'))
            auto_sharpen_value = config_parameters['AUTO_SHARPENING'].lower() == 'true'
            node_auto_sharpen.SetValue(auto_sharpen_value)

            if auto_sharpen_value == False:
                node_sharpening = ps.CIntegerPtr(nodemap.GetNode('Sharpening'))
                sharpening_value = config_parameters['SHARPENING']
                node_sharpening.SetValue(sharpening_value)

                node_sharpening_threshold = ps.CIntegerPtr('SharpeningThreshold')
                sharpening_threshold_value = config_parameters['SHARPENING_THRESHOLD']
                node_sharpening_threshold.SetValue(sharpening_threshold_value)

    except:
        pass
    #print( ps.CEnumerationPtr(nodemap.GetNode('PixelFormat')).GetCurrentEntry()
    #print(ps.CEnumerationPtr(nodemap.GetNode('AdcBitDepth')).GetValue())
        #Number of bins per pixel (1-4)
    vert_binning = ps.CIntegerPtr(nodemap.GetNode('BinningVertical'))
    vert_binning_to_set = 1
    vert_binning.SetValue(vert_binning_to_set)

    hoz_binning = ps.CIntegerPtr(nodemap.GetNode('BinningHorizontal'))
    hoz_binning_to_set = 1
    hoz_binning.SetValue(hoz_binning_to_set)

    node_decimation_hoz = ps.CIntegerPtr(nodemap.GetNode('DecimationHorizontal'))
    decimation_hoz = 1
    node_decimation_hoz.SetValue(decimation_hoz)

    node_decimation_vert = ps.CIntegerPtr(nodemap.GetNode('DecimationVertical'))
    decimation_vert = 1
    node_decimation_vert.SetValue(decimation_vert)

    node_ISP = ps.CBooleanPtr(nodemap.GetNode('IspEnable'))
    ISP_to_set = config_parameters['ISP'].lower() == "true"
    node_ISP.SetValue(ISP_to_set)

    node_binning_selector = ps.CEnumerationPtr(nodemap.GetNode('BinningSelector'))
    binning_selector_value = node_binning_selector.GetEntryByName(config_parameters['BINNING_SELECTOR'])
    node_binning_selector.SetIntValue(binning_selector_value.GetValue())
    #Whether binning is to be achieved through averaging or summing
    bin_vert_mode = ps.CEnumerationPtr(nodemap.GetNode('BinningVerticalMode'))
    node_bin_vert_sum = ps.CEnumEntryPtr(bin_vert_mode.GetEntryByName(config_parameters['BIN_METHOD']))
    bin_vert_mode.SetIntValue(node_bin_vert_sum.GetValue())

    bin_hoz_mode = ps.CEnumerationPtr(nodemap.GetNode('BinningHorizontalMode'))
    node_bin_hoz_sum = ps.CEnumEntryPtr(bin_hoz_mode.GetEntryByName(config_parameters['BIN_METHOD']))
    bin_hoz_mode.SetIntValue(node_bin_hoz_sum.GetValue())

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


    node_decimation_selector = ps.CEnumerationPtr(nodemap.GetNode('DecimationSelector'))
    decimation_selector_value = node_decimation_selector.GetEntryByName(config_parameters['DECIMATION_SELECTOR'])
    node_decimation_selector.SetIntValue(decimation_selector_value.GetValue())

    node_hoz_decimation_mode = ps.CEnumerationPtr(nodemap.GetNode('DecimationHorizontalMode'))
    decimation_mode = node_hoz_decimation_mode.GetEntryByName(config_parameters['DECIMATION_METHOD'])
    node_hoz_decimation_mode.SetIntValue(decimation_mode.GetValue())

    node_vert_decimation_mode = ps.CEnumerationPtr(nodemap.GetNode('DecimationVerticalMode'))
    decimation_mode = node_vert_decimation_mode.GetEntryByName(config_parameters['DECIMATION_METHOD'])
    node_vert_decimation_mode.SetIntValue(decimation_mode.GetValue())

    node_decimation_hoz = ps.CIntegerPtr(nodemap.GetNode('DecimationHorizontal'))
    decimation_hoz = config_parameters['DECIMATION']
    node_decimation_hoz.SetValue(decimation_hoz)

    node_decimation_vert = ps.CIntegerPtr(nodemap.GetNode('DecimationVertical'))
    decimation_vert = config_parameters['DECIMATION']
    node_decimation_vert.SetValue(decimation_vert)

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
    offsety_to_set = config_parameters['OFFSET_Y']
    node_offsety.SetValue(offsety_to_set)

    #Return the Frame rate of resulting from the acquisition parameters
    FPS_aq = ps.CFloatPtr(nodemap.GetNode('AcquisitionFrameRate')).GetValue()
    FPS_res = ps.CFloatPtr(nodemap.GetNode('AcquisitionResultingFrameRate')).GetValue()

    SN = ps.CStringPtr(nodemap.GetNode('DeviceSerialNumber')).GetValue()
    print(f'Generating log file for {SN}')

    write_log_file(nodemap, config_parameters, SN, output)

    #Change back to timed mode no matter what otherwise a background can't be taken
    node_exposure_mode = ps.CEnumerationPtr(nodemap.GetNode('ExposureMode'))
    exposure_mode_set = node_exposure_mode.GetEntryByName('Timed')
    node_exposure_mode.SetIntValue(exposure_mode_set.GetValue())

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
    return FPS_aq, FPS_res


def main(output, config_1, config_2):
    """
        Main function that takes in the config file and output directory
        the funtion initialises the camera and handles the acquisition,
        and saving of the images acquired.

        TDOD: This function would work better as 5 separate funtions
            1) Initilise camera
            2) Trigger mode function
            3) Time mode function
            4) Continuous mode funtion
            5) Uninitialise camera
        TODO: Have the option to save frame by frame or with accumulated acquisition for all operating types
        TODO: turn leading zeros into a function to call each time rather than copy paste
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
            print(f'Writing Camera {camera_SN} settings')

            #return the node map to set acquisition parameters
            nodemap_1 = cam_1.GetNodeMap()
            #Set the acquisiton paraeters and return the frame rate (see above function)
            FPS_aq, FPS_res = set_settings(nodemap_1, config_parameters_1, output)
            print(f'Camera 1 ({camera_SN}):')
            print(f"Acquisition Frame Rate: {round(FPS_aq,0)}   Resulting Frame Rate: {round(FPS_res,0)}")
        if mode == 'multi':
            if camera_SN == config_parameters_2['SERIAL_NUMBER']:
                print(f'Writing Camera {camera_SN} settings')
                #Define camera 1 as a camera object within the API and initilise it
                cam_2 = camera
                cam_2.Init()

                #return the node map to set acquisition parameters
                nodemap_2 = cam_2.GetNodeMap()
                #Set the acquisiton paraeters and return the frame rate (see above function)
                FPS_aq, FPS_res = set_settings(nodemap_2, config_parameters_2, output)
                print(f'Camera 2 ({camera_SN}):')
                print(f"Acquisition Frame Rate: {round(FPS_aq,0)}   Resulting Frame Rate: {round(FPS_res,0)}")

    cam_1.BeginAcquisition() # start acquisition
    if mode == 'multi':
        cam_2.BeginAcquisition()

    #Set intialial booleans reqired for acquisition logic
    acquiring = True # is acquiring
    i=0 #begin acquisition count
    first = True # required for determining first frame of an acquisition
    triggered = False #Acquisition trigger for trigger mode off
    start = True # for printing when data is being acquired for trigger mode
    if config_parameters_1["ACQUISITION_MODE"].lower() == 'external':
        timeout = (int) ((1./FPS_res) +10)
    else:
        timeout = (int)(cam_1.ExposureTime.GetValue() / 1000 + 10) #determines time between retrieving frames from the camera
    if (1./FPS_res) + 10 > timeout:
        #print(timeout)
        timeout = (int) ((1./FPS_res) +10) # for most cases exposure is the better time to use. This avoids errors trying to get images faster than the FPS
        #print(timeout)
    
    
    threshold_1 = 0. # Set threshold for trigger to zero
    threshold_2 = 0. # Set threshold for trigger to zero
    b=0 # set counter for number of background images at 0
    image_result_1 = cam_1.GetNextImage(timeout) #retrieve image from the camera after timeout
    image_data_1 = image_result_1.GetNDArray() #retrieve the array of image data
    bg_arr_1 = np.zeros(image_data_1.shape,dtype=np.float32) #set background array to match size of image array with value of 0
    
    if mode == 'multi':
        image_result_2 = cam_2.GetNextImage(timeout) #retrieve image from the camera after timeout
        image_data_2 = image_result_2.GetNDArray() #retrieve the array of image data
        bg_arr_2 = np.zeros(image_data_2.shape,dtype=np.float32) #set background array to match size of image array with value of 0
    external_3v = False
    t_end = time.time() + 10 # Set backqroung acquisition time (10s)
    percentile = 98
    if config_parameters_1["SKIP_BACKGROUND"].lower() !='yes':
        print('Acquiring Background')
        while time.time()<t_end: # Acquire backgroun averaging over t_end
            image_result_1 = cam_1.GetNextImage(timeout)
            image_data_1 = image_result_1.GetNDArray()
            bg_arr_1 += image_data_1 #add image data to background array
            threshold_1 += np.percentile(image_data_1, percentile) # Set add percentile of pixel values to the threshold
            image_result_1.Release() # release image to acquire the next one
            if mode == 'multi':
                image_result_2 = cam_2.GetNextImage(timeout)
                image_data_2 = image_result_2.GetNDArray()
                bg_arr_2 += image_data_2 #add image data to background array
                threshold_2 += np.percentile(image_data_2, percentile) # Set add percentile of pixel values to the threshold
                image_result_2.Release()
            b+=1 # increment counter to track number of images involved in background

        threshold_1 = (2*threshold_1)/b # average threshold over all background images
        threshold_2 = (2*threshold_2)/b # average threshold over all background images
    else:
        print('Background skipped')
        b=1
        threshold_1 = 0
        threshold_2 = 0
        
    np.save(output + config_parameters_1["CAMERA_VIEW"] + "/" + "Background" + ".npy", bg_arr_1/b) #save background array as a numpy .npy file
    if mode == 'multi':
        np.save(output + config_parameters_2["CAMERA_VIEW"] + "/" + "Background" + ".npy", bg_arr_2/b)

    print("Ready to acquire")

    if config_parameters_1['ACQUISITION_MODE'].lower() == 'external' or (mode == 'multi' and config_parameters_2['ACQUISITION_MODE'].lower == 'external'):
        cam_1.EndAcquisition()
        #Change back to timed mode no matter what otherwise a background can't be taken
        node_exposure_mode = ps.CEnumerationPtr(nodemap_1.GetNode('ExposureMode'))
        exposure_mode_set = node_exposure_mode.GetEntryByName(config_parameters_1['EXPOSURE_MODE'])
        node_exposure_mode.SetIntValue(exposure_mode_set.GetValue())
        node_trigger_mode = nodemap_1.GetNode('TriggerMode')
        #trigger_mode_set = node_trigger_mode.GetEntryByName('On')
        #node_trigger_mode.SetIntValue(trigger_mode_set.GetValue())
        cam_1.BeginAcquisition()
        if mode == 'multi':
            cam_2.EndAcquisition()
            node_exposure_mode = ps.CEnumerationPtr(nodemap_2.GetNode('ExposureMode'))
            exposure_mode_set = node_exposure_mode.GetEntryByName(config_parameters_2['EXPOSURE_MODE'])
            node_exposure_mode.SetIntValue(exposure_mode_set.GetValue())
            node_trigger_mode = nodemap_2.GetNode('TriggerMode')
            #trigger_mode_set = node_trigger_mode.GetEntryByName('On')
         #   node_trigger_mode.SetIntValue(trigger_mode_set.GetValue())
            cam_2.BeginAcquisition()
        


    #t_test_end = time.time() + 10 # used to test the frame rate over 10 seconds
    while acquiring: # will loop while acquiring is True
        ######################################################
        #               Software trigger                     #
        ######################################################
        if config_parameters_1['ACQUISITION_MODE'].lower() == 'trigger': # for acquisition mode trigger
            try: # This puts the whole process within a loop that ends after a keyboard interrupt (Ctrl + C)
                image_result_1 = cam_1.GetNextImage(timeout) #get image
                image_data_1 = image_result_1.GetNDArray() #return image array
                if mode == 'multi':
                    image_result_2 = cam_2.GetNextImage(timeout) #get image
                    image_data_2 = image_result_2.GetNDArray() #return image array
                if first: #for first image set the acquisition array to the same size full of zeros
                    arr_1 = np.zeros(image_data_1.shape)
                    if mode == 'multi':
                        arr_2 = np.zeros(image_data_2.shape)
                    first = False # no longer first acquisition
                    #print(np.percentile(image_data,99),threshold)
                if np.percentile(image_data_1,97) > threshold_1: #checks whether image data is above background levels (i.e. there is scintillation light)
                    if mode == 'multi':
                        if np.percentile(image_data_2,97) > threshold_2:
                            triggered = True # Start acquiring
                    else:
                        triggered = True # Start acquiring
                while triggered:
                    if start: # This ensures this statement only prints once per acquisition
                        print("Acquiring data")
                    start = False
                    image_result_1 = cam_1.GetNextImage(timeout) #Get image
                    image_data_1 = image_result_1.GetNDArray() # retunr image array
                    arr_1 = arr_1 + image_data_1 # add image array to acquisition array
                    if mode == 'multi':
                        image_result_2 = cam_2.GetNextImage(timeout) #Get image
                        image_data_2 = image_result_2.GetNDArray() # retunr image array
                        arr_2 = arr_2 + image_data_2 # add image array to acquisition array
                    if np.percentile(image_data_1,98) <= threshold_1: # checks if image data is below background (i.e. no scintillation light)
                        if i <10:
                            number = '0000' + str(i)
                        elif i < 100:
                            number = '000' + str(i)
                        elif i < 1000:
                            number = '00' +str(i)
                        elif i < 10000:
                            number =  '0' + str(i)
                        else:
                            number = str(i)
                        if mode == 'multi':
                            if np.percentile(image_data_2,98) <= threshold_2: # checks if image data is below background (i.e. no scintillation light)
                                triggered =False # stop acuisition
                                first = True # reset for next acquisition
                                start = True # reset for next acuquisition
                                print("Acqiusition stopped")
                                np.save(output + config_parameters_1["CAMERA_VIEW"] + "/" + "acquisition_" + number + ".npy", arr_1) # save as numpy .npy file
                                np.save(output + config_parameters_2["CAMERA_VIEW"] + "/" + "acquisition_" + number + ".npy", arr_2) # save as numpy .npy file
                                i+=1 #incremet the number of acquisitions for unique file names
                                print("image saved\n"
                                     "Ready to acquire")
                        else:
                            triggered =False # stop acuisition
                            first = True # reset for next acquisition
                            start = True # reset for next acuquisition
                            print("Acqiusition stopped")
                            np.save(output + config_parameters_1["CAMERA_VIEW"] + "/" + "acquisition_" + number + ".npy", arr_1) # save as numpy .npy file
                            i+=1 #incremet the number of acquisitions for unique file names
                            print("image saved\n"
                                 "Ready to acquire")
                    if triggered: # releases image to allow the next one if still triggered
                        image_result_1.Release()
                        if mode == 'multi':
                            image_result_2.Release()
                try: # trys to release the image to allow the next one if not triggered
                    image_result_1.Release()
                    if mode == 'multi':
                        try:
                            image_result_2.Release()
                        except:
                            pass
                except:
                    if mode == 'multi':
                        try:
                            image_result_2.Relese()
                        except:
                            pass
            except KeyboardInterrupt: # Stops acquisition session  when stop command entered (Ctrl + C)
                print("Acqiusition stopped")
                acquiring = False

        ######################################################
        #                          Timed                     #
        ######################################################
        elif config_parameters_1['ACQUISITION_MODE'].lower() == 'time': # acqisition mode timed - Frame by frame mode
            try:
                acquisition_time = config_parameters_1['ACQUISITON_TIME'] # retrive acquisition time from config file
                print("Press enter to acquire")
                input()
                t_stop = time.time() +  acquisition_time #sets the time at which the aquisition should end
                while time.time() < t_stop: # loops until the acquisition should end
                    if start:
                        print("Acquiring data")
                    start=False
                    image_result_1 = cam_1.GetNextImage(timeout) # Get image
                    image_data_1 = image_result_1.GetNDArray() # Return image array
                    if i <10:
                            number = '0000' + str(i)
                    elif i < 100:
                        number = '000' + str(i)
                    elif i < 1000:
                        number = '00' +str(i)
                    elif i < 10000:
                        number =  '0' + str(i)
                    else:
                        number = str(i)
                    if mode == 'multi':
                        image_result_2 = cam_2.GetNextImage(timeout) # Get image
                        image_data_2 = image_result_2.GetNDArray()
                    np.save(output + config_parameters_1["CAMERA_VIEW"] + "/" + "frame_" + number + ".npy", image_data_1) # save image as numpy .npy file
                    if mode == 'multi':
                        np.save(output + config_parameters_2["CAMERA_VIEW"] + "/" + "frame_" + number + ".npy", image_data_2) # save image as numpy .npy file
                    i+=1 # increment the acquisition counter for unique file names
                    image_result_1.Release() # release image so the next one can be allowed to be read
                    if mode == 'multi':
                        image_result_2.Release() # release image so the next one can be allowed to be read
                print("Acqiusition stopped")
                acquiring = False # Stops acquiring after the set time

            except KeyboardInterrupt:
                print("Acqiusition stopped")
                acquiring = False
        ######################################################
        #               Continuous                           #
        ######################################################
        elif config_parameters_1['ACQUISITION_MODE'].lower() == 'continuous': # acquires until stop command (Ctrl + C)
            try: # Sets up ability to stop acquisition on stop command
                if start:
                    input()
                    print("Acquiring data")
                start=False
                image_result_1 = cam_1.GetNextImage(timeout) # Get image
                image_data_1 = image_result_1.GetNDArray() # Return image array
                if i <10:
                    number = '0000' + str(i)
                elif i < 100:
                    number = '000' + str(i)
                elif i < 1000:
                    number = '00' +str(i)
                elif i < 10000:
                    number =  '0' + str(i)
                else:
                    number = str(i)
                np.save(output + config_parameters_1["CAMERA_VIEW"] + "/" + "frame_" + number + ".npy", image_data_1) #save image as numpy .npy file
                if mode == 'multi':
                    image_result_2 = cam_2.GetNextImage(timeout)
                    image_data_2 = image_result_2.GetNDArray()
                    np.save(output + config_parameters_2["CAMERA_VIEW"] + "/" + "frame_" + number + ".npy", image_data_2)
                i+=1 # increment acquisition counter for unique file names
                image_result_1.Release() # release image so the next one can be read
                if mode == 'multi':
                    image_result_2.Release()
            except KeyboardInterrupt: # stops acquisition on the stop command (Ctrl + C)
                acquiring = False
                print("Acqiusition stopped")

        ######################################################
        #               External trigger                     #
        ######################################################
        elif config_parameters_1['ACQUISITION_MODE'].lower() == 'external':
            try:
                if external_3v == False:
                    if config_parameters_1['SERIAL_NUMBER'] == '21119929':
                        node_line_selector = ps.CEnumerationPtr(nodemap_1.GetNode('LineSelector'))

                        line_output = node_line_selector.GetEntryByName('Line5')
                        node_line_selector.SetIntValue(line_output.GetValue())
                        node_user_output_select = ps.CEnumerationPtr(nodemap_1.GetNode('UserOutputSelector'))
                        line2_value = node_user_output_select.GetEntryByName("UserOutput2")
                        node_user_output_select.SetIntValue(line2_value.GetValue())
                        node_user_output_value = ps.CBooleanPtr(nodemap_1.GetNode('UserOutputValue'))
                        user_output_value = True
                        node_user_output_value.SetValue(user_output_value)
                        
                        line_output = node_line_selector.GetEntryByName('Line2')
                        node_line_selector.SetIntValue(line_output.GetValue())
                        node_line_mode = ps.CEnumerationPtr(nodemap_1.GetNode('LineMode'))
                        line_mode_output = node_line_mode.GetEntryByName('Output')
                        node_line_mode.SetIntValue(line_mode_output.GetValue())

                        line_3v = node_line_selector.GetEntryByName('Line6')
                        node_line_selector.SetIntValue(line_3v.GetValue())
                        node_3v = ps.CBooleanPtr(nodemap_1.GetNode('V3_3Enable'))
                        on_3v = True
                        node_3v.SetValue(on_3v)

                    if mode == 'multi':
                        if config_parameters_2['SERIAL_NUMBER'] == '21119929':
                            node_line_selector = ps.CEnumerationPtr(nodemap_2.GetNode('LineSelector'))
                            
                            line_output = node_line_selector.GetEntryByName('Line5')
                            node_line_selector.SetIntValue(line_output.GetValue())
                            node_user_output_select = ps.CEnumerationPtr(nodemap_2.GetNode('UserOutputSelector'))
                            line2_value = node_user_output_select.GetEntryByName("UserOutput2")
                            node_user_output_select.SetIntValue(line2_value.GetValue())
                            node_user_output_value = ps.CBooleanPtr(nodemap_2.GetNode('UserOutputValue'))
                            user_output_value = True
                            node_user_output_value.SetValue(user_output_value)

                            line_output = node_line_selector.GetEntryByName('Line2')
                            node_line_selector.SetIntValue(line_output.GetValue())
                            node_line_mode = ps.CEnumerationPtr(nodemap_2.GetNode('LineMode'))
                            line_mode_output = node_line_mode.GetEntryByName('Output')
                            node_line_mode.SetIntValue(line_mode_output.GetValue())

                            line_3v = node_line_selector.GetEntryByName('Line6')
                            node_line_selector.SetIntValue(line_3v.GetValue())
                            node_3v = ps.CBooleanPtr(nodemap_2.GetNode('V3_3Enable'))
                            on_3v = True
                            node_3v.SetValue(on_3v)
                    external_3v = True
                    
                    print("Trigger Ready")
                image_result_1 = cam_1.GetNextImage(300000000) #get image
                if mode == 'multi':
                    image_result_2 = cam_2.GetNextImage(300000000)
                image_data_1 = image_result_1.GetNDArray() #return image array
                if mode == 'multi':
                    image_data_2 = image_result_2.GetNDArray()
                if i <10:
                    number = '0000' + str(i)
                elif i < 100:
                    number = '000' + str(i)
                elif i < 1000:
                    number = '00' +str(i)
                elif i < 10000:
                    number =  '0' + str(i)
                else:
                    number = str(i)
                np.save(output + config_parameters_1["CAMERA_VIEW"] + "/" + "acquisition_" + number + ".npy", image_data_1) # save as numpy .npy file
                if mode == 'multi':
                    np.save(output + config_parameters_2["CAMERA_VIEW"] + "/" + "acquisition_" + number + '.npy', image_data_2)
                i+=1 #incremet the number of acquisitions for unique file names
                print("Image saved")
                image_result_1.Release()
                if mode == 'multi':
                    image_result_2.Release()

            except KeyboardInterrupt:
                acquiring = False
                print("Acquisition Stopped")

        else: # Stops session when no valid acquisition mode is in the config file
            print("Invalid acquisition mode")
            acquiring = False

    print("\nEnd of session")

    # These commands disconnect the camera and end the PySpin connection removing residual data
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



#Checks the number of arguments entered is acceptable
if len(sys.argv) < 3:
    #provides argument information if this is not the case
    print('Please enter the following arguments:\n'
    '1) Path to the configuration file(s)\n'
    '2) Path to output directory\n')

elif len(sys.argv) ==3:
    main(sys.argv[2], sys.argv[1], 'pass')
else: # runs main function
    main(sys.argv[3], sys.argv[1], sys.argv[2])
