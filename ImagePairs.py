"""
将属于同一层厚的图片放置同一文件夹中
从同一文件夹中任意选择两张图片形成一个npz文件
"""
import os
import pydicom
import SimpleITK as SItk
import dcm_process_demo as preprocess
import numpy as np


CT_Folder_Path = "C:/Users/lpw007/Desktop/CTScans/"
New_Image_Path = "C:/Users/lpw007/Desktop/NewImage/"


# ------------------------------  将属于同一层厚的图片放置同一文件夹中 --------------------------------
# start_pos = 105
# while start_pos <= 295:
#     folder = os.path.join(New_Image_Path, str(start_pos))
#     count = 1
#     for i in range(1, 13):
#         slices_path = os.path.join(CT_Folder_Path, str(i))
#         print(slices_path)
#         # 遍历其中所有切片 并将其中TP值再start_pos附近的移动到对应的目录中去
#         for s in os.listdir(slices_path):
#             image = pydicom.read_file(os.path.join(slices_path, s))
#             TP = image.SliceLocation
#             if TP < float(start_pos + 2.5) and TP > float(start_pos - 2.5):
#                 new_name = str(start_pos) + '_' + str(count) + '.dcm'
#                 os.rename(os.path.join(slices_path, s), os.path.join(folder, new_name))
#                 count += 1
#     print(start_pos)
#     start_pos += 5
# -------------------------------------------------------------------------
New_Image_Path = "C:/Users/lpw007/Desktop/NewImage"
NPZ_Path = "C:/Users/lpw007/Desktop/ScanNPZ"
NPZ_Path1 = "C:/Users/lpw007/Desktop/ScanNPZ1"
start_pos = 105

while start_pos <= 295:
    folder = os.path.join(New_Image_Path, str(start_pos))
    if not os.path.exists(os.path.join(NPZ_Path, str(start_pos))):
        os.mkdir(os.path.join(NPZ_Path, str(start_pos)))
    slices = [pydicom.read_file(folder + '/' + s) for s in os.listdir(folder)]

    slices.sort(key=lambda x: int(x.SliceLocation))  # 按照层厚扫描时期排序
    if len(slices)%2 != 0:
        slices = slices[0:-1]  # 删除最后一个元素
        ct_pixels = preprocess.get_pixels_hu(slices)
    for i in range(int(ct_pixels.shape[0]/2)):  # 按照顺序两两放到一个npz文件中
        ''' 下面进行预处理 '''
        img1 = ct_pixels[i*2]
        img2 = ct_pixels[i*2 + 1]
        img1 = preprocess.transform_CtData(img1, normal=True)
        img2 = preprocess.transform_CtData(img2, normal=True)
        data_list = list()
        data_list.append(img1)
        data_list.append(img2)
        data = np.stack(data_list)
        np.savez(os.path.join(NPZ_Path1, str(start_pos) + '_' + str(i + 1)), data)
    start_pos += 5












