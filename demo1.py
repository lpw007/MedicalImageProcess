import os
import numpy as np

import matplotlib.pyplot as plt

New_Image_Path = "C:/Users/lpw007/Desktop/NewImage"
NPZ_Path = "C:/Users/lpw007/Desktop/ScanNPZ"
start_pos = 195

folder = os.path.join(NPZ_Path, str(start_pos))
npzfiles = os.listdir(folder)
npz_file = np.load(folder + '/' + npzfiles[0])
print(npz_file['arr_0'].shape)
plt.figure('HuImage')
plt.imshow(npz_file['arr_0'], cmap='gray')
plt.show()



