import h5py
import os
import numpy as np


class HDF5DatasetGenerator:
    """
    用于生成h5格式的数据
    """
    def __init__(self, dbPath, batchSize, preprocessors=None, aug=None, binarize=None):
        """
        定义h5文件的生成器作为网络的输入生成器
        :param dbPath: h5文件路径
        :param batchSize:
        :param preprocessors: 预处理器集合，包含多个预处理方法
        :param aug:
        :param binarize:
        """
        self.batchsize = batchSize
        self.preprocessors = preprocessors
        self.aug = aug
        self.binarize = binarize

        self.db = h5py.File(dbPath)
        self.numImages = self.db["movingImage"].shape[0]
        print("total images:",  self.numImages)
        self.num_batches_per_epoch = int((self.numImages - 1) / batchSize) + 1

    def generator(self, shuffle=True, passes=np.inf):
        epochs = 0

        while epochs < passes:
            shuffle_indices = np.arange(self.numImages)
            shuffle_indices = np.random.permutation(shuffle_indices)
            for batch_num in range(self.num_batches_per_epoch):
                start_index = batch_num * self.batchsize
                end_index = min((batch_num + 1)*self.batchsize, self.numImages)

                batch_indices = sorted(list(shuffle_indices[start_index:end_index]))

                movingImages = self.db["movingImage"][batch_indices, :, :, :]
                fixedImages = self.db["fixedImage"][batch_indices, :, :, :]

                # 对图片进行预处理
                if self.preprocessors is not None:
                    procMovingImages = []
                    procFixedImages = []
                    for image in movingImages:
                        for p in self.preprocessors:
                            image = p.preprocess(image)
                            procMovingImages.append(image)

                    movingImages = np.array(procMovingImages)

                    for image in fixedImages:
                        for p in self.preprocessors:
                            image = p.preprocess(image)
                            procFixedImages.append(image)

                    fixedImages = np.array(procFixedImages)

                if self.aug is not None:
                    (movingImages, fixedImages) = next(self.aug.flow(movingImages, movingImages, batch_size=self.batchSize))

                yield (movingImages, fixedImages)

            epochs += 1

    def close(self):
        self.db.close()



