import numpy as np
import sys
import glob

frames = glob.glob(sys.argv[1] + 'frame*')
image_number = sys.argv[2]

image = np.zeros(np.load(frames[0]).shape)
i=0
for frame in frames:
    image += np.load(frame)
    i+= 1

image =image/i

np.save("./images/cal_image" + str(image_number) + ".npy", image)
