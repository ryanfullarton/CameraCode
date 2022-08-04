import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

"""
    A script to plot any 2D numpy array is grayscale
    By clicking anywhere on a canvas a plot of the x and y profile through that point can be made
"""


def pixel_select(event):
    fig, ax=plt.subplots()
    x=int(event.xdata)
    y=int(event.ydata)
    ax.plot(np.flip(a[:,x]),label='y')
    ax.plot(a[y,:], label = 'x')
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    #ax.set_title("Lateral Profile")
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', width=1)
    ax.tick_params(which='major', length=7)
    ax.tick_params(which='minor', length=4)
    ax.grid(linestyle ='--')
    plt.legend()
    plt.show()

    #plt.Figure()
    #plt.imshow(a,cmap='gray')
    #plt.plot([0,len(a[y,:])],[y,y])
    #plt.plot([x,x],[0,len(a[:,x])])
    #plt.axis('off')
    #plt.show()

a = np.load(sys.argv[1])


fig, ax= plt.subplots()
fig.subplots_adjust(wspace=0.03)
fig.canvas.mpl_connect('button_press_event', pixel_select)
ax.imshow(a, cmap ='gray')
ax.axis('off')
plt.show()
