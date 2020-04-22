import SimpleITK as sitk
import numpy as np

import skimage.io as io
import matplotlib.pyplot as plt

import gzip

import os

root_path = 'F://adni//ADNI1_Screening_1.5T_5//ADNI'

all_file = []
def get_all_file(root_dir):
    for f in os.listdir(root_dir):
        file_path = os.path.join(root_dir, f)
        file_path =  eval(repr(file_path).replace('\\','/'))
        if os.path.isdir(file_path):
            get_all_file(file_path)
        else:
            if os.path.splitext(file_path)[1] == '.nii':
                all_file.append(file_path)
    return all_file

def un_gz(filename, new_name):
    """
    解压.gz文件
    :param filename:
    :return:
    """
    # f_name = filename.replace(".gz", "")  # 得到解压后的文件名
    g_file = gzip.GzipFile(filename)  # 获得原始压缩文件
    f_name = new_name
    # g_file = gzip.decompress(g_file.read())
    open(f_name, "wb").write(g_file.read())  # 写入解压后的文件
    g_file.close()

# if __name__ == '__main__':
#     all_files = get_all_file(root_path)
#     for path in all_files:
#         strs = path.split('//')
#         new_name = strs[3] + strs[4] + '.nii'
#         # print(new_name)
#         new_name = os.path.join('E:/niidata6',new_name)
#         un_gz(path, new_name)
if __name__ == '__main__':
    all_files = get_all_file(root_path)
    for path in all_files:
        # print(path)
        strs = path.split('//')
        fileName = strs[-1]
        new_name = os.path.join('F:/NiiData', fileName)
        os.rename(path, new_name)









