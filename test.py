import numpy as np

array = np.arange(1,7).reshape(2,3)
print(array)

mask = np.zeros((2,3))
mask = mask > 1
print(mask)
mask[1,2] = True
print(array[mask])