import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os
import PIL
import cv2


if len(sys.argv) <3:
    print("Enter file directory and indicate whether to convert to tiff (1) or not (2)")

else:
    files = glob.glob(sys.argv[1] + 'a*.npy')
    files.sort()
    print(files)

    #print(files)
    if sys.argv[2] == '1':
        try:
            os.mkdir(sys.argv[1]+ "tiff/")
        except FileExistsError:
            pass
   
    for file in files:
        im = np.int32(np.load(file))
        plt.imshow(im)
        plt.title(file.split('/')[-1][0:-4])
        plt.pause(0.004)
        plt.clf()

        print(file.split('/')[-1])
        old_num = int(file.split('/')[-1][12:-4])

        if sys.argv[2] == '1':
            if old_num<10:
                new_name = file.split('/')[-1][0:-5] + '00' + str(old_num)
            elif old_num < 100:
                new_name = file.split('/')[-1][0:-6] + '0' +str(old_num)
            else:
                new_name = file.split('/')[-1][0:-7] + str(old_num)
            im = im/im.max()
            im*=255
            im = im.astype(np.uint8)
            print('Saved: ' + '/'.join(file.split('/')[0:-1]) +'/tiff/' + new_name + '.tiff')
            cv2.imwrite('/'.join(file.split('/')[0:-1]) +'/tiff/'  + new_name + '.tiff', im)
        
    
