import os

import SimpleITK as sitk
import numpy as np

import nibabel as nib

import skimage.io as io
import matplotlib.pyplot as plt

path = 'F:/result'
save_path = 'E:/npzFile'

for file in os.listdir(path):
    file_name = os.path.join(path, file)
    # print(file_name)
    # data = sitk.ReadImage(file_name)
    # img = sitk.GetArrayFromImage(data)  # 得到256*256*256的三维图像
    # 进行归一化
    img = nib.load(file_name).get_data()
    img = img.copy()
    print('输出值范围',np.max(img), np.min(img))
    img[img>256] = 255
    img[img<0] = 0
    img = img/255
    # 进行裁剪 裁成(160, 192, 224)
    img = img[48:-48, 31:-33, 3:-29]
    npz_name = file_name.split('\\')[-1].split('.')[0]
    npz_name = os.path.join(save_path, npz_name)
    np.savez("{}.npz".format(npz_name), vol=img)

    # print(npz_name)

    # print(img.shape)
    # plt.figure('data')
    # plt.imshow(img[:,:,125], cmap='gray')
    # plt.show()
    # 输出为npz格式的数据

# if __name__ == '__main__':
#     path = 'E:/npzFile'
#     file = os.listdir(path)
#     file_name = os.path.join(path, file[0])
#     data = np.load(file_name)
#     plt.figure('data')
#     plt.imshow(data['vol'][:,:,125], cmap='gray')
#     plt.show()

