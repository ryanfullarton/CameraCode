import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os
import PIL
import cv2


maindir = sys.argv[1]
latdir = maindir +'/Lateral/'
distdir = maindir +'/Distal/'
topdir = maindir +'/Top/'

lat_files = glob.glob(latdir + '*.npy')
top_files = glob.glob(topdir + '*.npy')
dist_files = glob.glob(distdir + '*.npy')
lat_files.sort()
top_files.sort()
dist_files.sort()

#print(files)        
if len(sys.argv) > 1:
    delay = float(sys.argv[2])
else:
    delay = 0.05
fig,ax = plt.subplots(2,2, figsize=(12,10))
for i in range(0,len(lat_files)):
    lat_im = np.int32(np.load(lat_files[i]))
    dist_im = np.int32(np.load(dist_files[i]))
    top_im = np.int32(np.load(top_files[i]))
    ax[0,0].imshow(top_im, vmin=0)
    ax[1,0].imshow(lat_im,vmin=0)
    ax[1,1].imshow(dist_im,vmin=0)
    ax[0,1].set_axis_off()
    fig.suptitle(lat_files[i].split('/')[-1][0:-4])
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(delay)
    ax[0,0].cla()
    ax[1,0].cla()
    ax[1,1].cla()

    