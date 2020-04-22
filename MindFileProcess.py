"""
 自动解压.gz文件
"""
import gzip
import os
# import tarfile

def un_gz(filename):
    """
    解压.gz文件
    :param filename:
    :return:
    """
    f_name = filename.replace(".gz", "")  # 得到解压后的文件名
    g_file = gzip.GzipFile(filename)  # 获得原始压缩文件
    # g_file = gzip.decompress(g_file.read())
    open(f_name, "wb").write(g_file.read())  # 写入解压后的文件
    g_file.close()


root_path = 'E:\ANDI\ADNI1_Annual_2_Yr_1.5T_1\ADNI'

for folder in os.listdir(root_path):
    data_folder = os.path.join(root_path, folder)  # 得到子数据集的子目录
    for sub_folder in os.listdir(data_folder):
        file_folder = os.path.join(data_folder, sub_folder)
        for file_folder1 in os.listdir(file_folder):
            nii_folder = os.path.join(file_folder, file_folder1)
            # print(nii_folder)
            for file in os.listdir(nii_folder):
                # print(file)
                if os.path.splitext(file)[1] == '.nii':  # 如果是.gz文件
                    # if file.split('.')[0] != 'labels':
                    file_name = os.path.join(nii_folder, file)
                    file_name = eval(repr(file_name).replace('\\', '/'))
                    print(file_name)
                    # print(file_name)
                    # un_gz(file_name)  # 解压文件
                    new_name = os.path.join('E:/NiiData', file)
                    # print(new_name)
#                     new_name = eval(repr(new_name).replace('\\', '/'))
#                     os.rename(file_name, new_name)
# # if __name__ == '__main__':
#     un_gz('E://配准数据//MIND数据集//individual//Volumes//Extra-18_volumes//Afterthought-1//t1weighted.MNI152.nii.gz')


