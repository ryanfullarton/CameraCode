import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from PIL import Image
import skimage.io
import glob
import os
plt.rcParams['image.cmap'] = 'gray'

files = glob.glob(sys.argv[1] +'*.pgm')
files = sorted(files)
path = sys.argv[1] + 'converted/'
print(path)
try:
    os.mkdir(path)
except:
    pass

i = 0
for file in files:
    
    image = skimage.io.imread(file)
    print(image.shape[0])
    if i <10:
        np.save(path + f'acquisition_00{i}.npy',image)
    elif i<100:
        np.save(path + f'acquisition_0{i}.npy',image)
    else:
        np.save(path + f'acquisition_{i}.npy',image)
    if i == 0:
        total = np.zeros((image.shape[0],image.shape[1]-100))
    total = total + (image[:,100:])


    if i <10:
        plt.imsave(path + f'sum/total_00{i}.png', total)
    elif i<100:
        plt.imsave(path + f'sum/total_0{i}.png', total)
    else:
        plt.imsave(path + f'sum/total_{i}.png', total)



    i+=1

plt.imshow(total, vmax = np.percentile(total,99))
np.save(path + 'total.npy', total)
plt.show()