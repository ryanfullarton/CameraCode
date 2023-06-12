import glob
import numpy as np
import matplotlib.pyplot as plt
import sys


file_list = glob.glob(sys.argv[1] + 'acquisition*' )
bg = np.load(sys.argv[1]+'Background.npy')
first = np.load(file_list[0])

final = np.zeros(first.shape)

for file in file_list[0:150]:
    arr = np.load(file)
    final = final + arr - bg
np.save(sys.argv[1]+ 'accummulated.npy', final)
plt.imshow(final, cmap ='gray', vmin = 0)
plt.show()