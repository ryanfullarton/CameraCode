import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from PIL import Image
import skimage.io

def pixel_select(event):
    fig, ax=plt.subplots()
    x=int(event.xdata)
    y=int(event.ydata)
    ax.plot(np.flip(a[:,x]),label='y')
    ax.plot(a[y,:], label = 'x')
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=4)
    ax.grid(linestyle ='--')
    plt.legend()
    plt.show()



image = skimage.io.imread(sys.argv[1])

#image.show() 
#a = np.array(image.getdata(),dtype=np.float16).reshape(image.size[1], image.size[0])
#a = np.asarray(image, dtype = np.int32)
#a.astype(int)
#print(image.mode)
a=image
print(image.dtype)
fig, ax= plt.subplots()
fig.subplots_adjust(wspace=0.03)
fig.canvas.mpl_connect('button_press_event', pixel_select)
ax.imshow(a,cmap='gray', vmin =0)
ax.axis('off')
plt.show()
