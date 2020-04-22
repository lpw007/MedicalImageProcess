"""
 this sciript for MRI .img format
"""

import SimpleITK as sitk
import numpy as np

import os

ori_path = 'E:\配准数据\LPBA40'
new_path = 'C:\\Users\lpw007\Desktop\LPBA'


for sub_dir in os.listdir(new_path):
    temp_path = os.path.join(new_path, sub_dir)
    for file in os.listdir(temp_path):
        file_name = temp_path + '\\' + file
        print(file_name)
        image = sitk.ReadImage(file_name)
        print(image)

