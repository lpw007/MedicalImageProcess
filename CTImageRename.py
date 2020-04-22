import os
import pydicom

input_path = "C:/Users/lpw007/Desktop/CTImage/"

for i in range(2, 16):
    if i == 9:
        continue
    ct_files_path = input_path + str(i) + "/"
    ct_lists = os.listdir(ct_files_path)
    for j in range(len(ct_lists)):
        slice = pydicom.dcmread(ct_files_path + ct_lists[j])
        num = int(slice.InstanceNumber)
        os.rename(ct_files_path + ct_lists[j], ct_files_path + str(num) + '.dcm')
