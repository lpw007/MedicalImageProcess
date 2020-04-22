import h5py
import os


class HDF5DatasetWriter:
    def __init__(self, movingImages_dims, fixedImage_dims, outputPath, bufSize=200):
        """
        :param movingImages_dims: 浮动图像的维度
        :param fixedImage_dims: 固定图像的维度
        :param outputPath:
        :param bufSize: 当内存储存了 bufSize个数据时， 就需要flush到外存
        """
        if os.path.exists(outputPath):
            raise ValueError("The outputpath already exists")
        self.db = h5py.File(outputPath, 'w')
        self.movingImg = self.db.create_dataset("movingImage", movingImages_dims, maxshape=(None,)+movingImages_dims[1:], dtype="float")
        self.fixedImg = self.db.create_dataset("fixedImage", fixedImage_dims, maxshape=(None,)+fixedImage_dims[1:], dtype="float")
        self.dims = movingImages_dims
        self.bufSize = bufSize
        self.buffer = {"movingImage": [], "fixedImage": []}
        self.idx = 0

    def add(self, movingDatas, fixedDatas):
        """
        向对应的dataset中添加数据
        :param movingDatas:
        :param fixedDatas:
        :return:
        """
        # 先将数据添加到缓存中
        self.buffer["movingImage"].extend(movingDatas)
        self.buffer["fixedImage"].extend(movingDatas)
        print("len ", len(self.buffer["movingImage"]))

        if len(self.buffer["movingImage"]) >= self.bufSize:
            self.flush()

    def flush(self):
        """
        当超过buhher时将数据输出到
        :return:
        """
        i = self.idx + len(self.buffer["movingImage"])
        if i > self.movingImg.shape[0]:  # 如果i值超过dataset的shape则扩大dataset的容量
            # 自定义扩展大小
            new_shape = (self.movingImg.shape[0]*2, ) + self.dims[1:]
            print('resize to new_shape:', new_shape)
            self.movingImg.resize(new_shape)
            self.fixedImg.resize(new_shape)
        # 将buffer中的数据输出到dataset中
        self.movingImg[self.idx:i, :, :, :] = self.buffer['movingImg']
        self.fixedImg[self.idx:i, :, :, :] = self.buffer['fixedImg']
        print("h5py have writen %d data" % i)
        self.idx = i
        self.buffer = {"movingImage": [], "fixedImage": []}  # 清空buffer

    def close(self):
        if len(self.buffer["movingImage"]) > 0:  # 将buffer中的数据输出
            self.flush()



