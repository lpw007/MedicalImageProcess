"""
对于CT图像的预处理, 步骤如下：
    1、 利用dicom从dcm格式中读取数组格式的数据
    2、 将读取的CT值转化为标准的hu值
    3、 进行windowing操作(hu值范围较大，导致对比度很差)
    4、 进行重采样(可能不同scan的扫描面不一样，因此先进行同构采样)
    4、
"""
import glob
import os
import pandas as pd
import SimpleITK as sitk

import numpy as np

import pydicom as dicom
import matplotlib.pyplot as plt
import scipy.ndimage.interpolation as sci_interpolation

from skimage import measure, feature
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def load_scan(path):
    """
    载入扫描面
    :param path: dcm文件路径 其中包含多个dcm文件
    :return: 切片的列表
    """
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]  # 使用dicom读取dcm文件
    '''
    ImagePositionPatient为CT切片的属性 描述当前CT切片在最左下角点在整个三维扫描体系中的坐标 如['-270.0032', '-270.0032', '8.0000']
    下一行代码按8.000排序 也就是按照z轴来排
    '''
    # slices.sort(key=lambda x: int(x.ImagePositionPatient[2]))

    # 计算切片的厚度 两切片之间的间隔(如果SliceThickness 属性缺失的话可以这样估算)
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    return slices


def get_pixels_hu(slices):
    """
    将CT的灰度值转化为HU单元
    计算公式为：Hounsfield Unit = pixel_value * rescale_slope + rescale_intercept
    首先去除灰度值为-2000的pixel_array CT扫描边界之外的灰度值固定为-2000
    设定这些值为0，当前对应为空气（值为0）
    :param slices:
    :return:
    """
    image = np.stack([s.pixel_array for s in slices])  # image.shape为(229, 512, 512)
    # 转为int16
    image = image.astype(np.int16)

    # 将CT值为2000的设为0
    image[image == -2000] = 0

    # 计算HU值
    for number in range(len(slices)):
        # 获取属性RRescaleIntercept以及Rescaleslope
        intercept = slices[number].RescaleIntercept
        slope = slices[number].RescaleSlope

        if slope != 1:  # 一般情况下rescale slope = 1, intercept = -1024
            image[number] = slope * image[number].astype(np.float16)
            image[number] = image[number].astype(np.int16)

        image[number] += np.int16(intercept)

    return np.array(image, dtype=np.int16)


def resample(image, scan, new_spacing=[1, 1, 1]):
    """
    对扫描面的像素进行重采样
        由于不同扫描面的像素尺寸、粗细粒度是不同的，因此需要进行重构采样
    默认采样大小为[1mm, 1mm, 1mm]
    :return: 重采样之后的数据
    """
    # 首先确定当前Space
    spacing = map(float, ([scan[0].SliceThickness] + list(scan[0].PixelSpacing)))  # 将对应属性的值float
    spacing = np.array(list(spacing))

    # 计算放缩因子
    new_spacing = np.array(new_spacing)
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = sci_interpolation.zoom(image, real_resize_factor, mode='nearest')

    return image, new_spacing


def plot_3d(image, threshold=-300):
    """
    将CT序列输出成三维图像
    :param image:
    :param threshold:
    :return:
    """
    # 将人竖立
    p = image.transpose(2, 1, 0)

    verts, faces = measure.marching_cubes_lewiner(p, threshold)  #
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.1)
    face_color = [0.5, 0.5, 1]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)
    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])
    plt.show()


def plot_ct_scan(scan):
    """
    输出一个scan中的所有序列
    :param scan:
    :return:
    """
    f, plots = plt.subplots(int(scan.shape[0] / 20) + 1, 4, figsize=(50, 50))
    for i in range(0, scan.shape[0], 5):
        plots[int(i / 20), int((i % 20) / 5)].axis('off')
        plots[int(i / 20), int((i % 20) / 5)].imshow(scan[i], cmap=plt.cm.bone)


def transform_data(image, normal=False, range=[-2000, 1000]):
    """
    对应步骤三 使用windowing进行对比增强 image为转为hu值之后的数据数组
    :param windowWidth: 表示ct图中包含的ct值的范围(往往窗口值过大会导致模糊)
    :param windowCenter: ct值的中点（值越大，图片往往越暗）
    :param normal: normal之前 ct被归一到0-1范围 normal使其成为255的像素值
    :return:
    """
    max_hu = range[1]
    min_hu = range[0]
    windowWidth = max_hu - min_hu  # 计算hu值的范围
    windowCenter = 0.5*float(windowWidth)

    minWindow = float(windowCenter) - 0.5*float(windowWidth)
    newimg = (image - minWindow) / float(windowWidth)
    newimg[newimg < 0] = 0
    newimg[newimg > 1] = 1
    if not normal:
        newimg = (newimg*255).astype('uint8')
    return newimg


def transform_CtData(image, normal=False, zero_mean=False, range=[-2000, 1000]):
    """
    数据归一化
    :param image: 图像
    :param normal: 是否归一化 不归一化则*255
    :param range: 像素值范围
    :return:
    """
    MIN_BOUND = range[0]
    MAX_BOUND = range[1]
    image = (image - MIN_BOUND)/(MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1
    image[image < 0] = 0
    if zero_mean:
        pixels_mean = np.mean(image)
        image = image - pixels_mean  # 去零均值化
    if not normal:
        image = (image * 255.).astype('uint8')
    return image


if __name__ == '__main__':
    path = 'C:/Users/lpw007/Desktop/CTScans/2'
    slices = load_scan(path)
    print(slices[0].pixel_array.shape)
    # ct_pixels = get_pixels_hu(slices)
    # plt.figure('HuImage')
    # plt.imshow(ct_pixels[10], cmap='gray')
    # plt.figure('WindowConvert')
    # plt.imshow(transform_data(ct_pixels[10], normal=True), cmap='gray')
    # plt.figure('ConvertCT')
    # plt.imshow(transform_CtData(ct_pixels[10], normal=True), cmap='gray')
    # plt.figure('ConvertCT_Zero')
    # plt.imshow(transform_CtData(ct_pixels[10], normal=True, zero_mean=True), cmap='gray')
    # print(ct_pixels[10])
    # print(ct_pixels.shape)
    # pixel_resample, spacing = resample(ct_pixels, slices, [1, 1, 1])
    # plt.figure('InitialImage')
    # plt.imshow(slices[10].pixel_array, cmap='gray')
    # plt.figure('ResampleImage')
    # plt.imshow(pixel_resample[50], cmap='gray')
    # print(pixel_resample.shape)
    # plt.show()










