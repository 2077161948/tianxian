import cv2
import numpy as np
import imagehash
from PIL import Image


class image_service:

    def __init__(self, file_model):
        self.file_model = file_model

    def resize(self, length, width):
        # 重新改变图片大小
        image = self.file_model.image_file_buff
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        resize = cv2.resize(image, (length, width))
        return resize

    def image_similarity(self):
        #计算图片相识度
        image = self.file_model.image_file_buff
        image = cv2.imread(image)
        type = self.file_model.type
        image_list = self.file_model.image_file_list
        result = []
        for item in image_list:
            item_image = cv2.imread(item)
            similarity = 0
            if type is None or type == 0:
                similarity = self.mse(image, item_image)
            elif type == 1:
                similarity = self.mse(image, item_image)
            else:
                similarity = self.hamming_distance(self.dhash(image), self.dhash(item_image))
            result.append(similarity)
        return result

    def superposition(self):
        #图片叠加
        image = self.file_model.image_file_buff
        image = cv2.imread(image)

    def mse(self, image1, image2):
        # 计算均方误差
        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image1.shape[1])
        return err

    def hist_compare(self, image1, image2):
        # 计算直方图比较方法的相似度
        hist1 = cv2.calcHist([image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    def hamming_distance(self, hash1, hash2, hash_size=8):
        distance = hash1 - hash2
        similarity = 1 - (distance / (hash_size * hash_size))
        return similarity

    def dhash(self, image, hash_size=8):
        return imagehash.average_hash(Image.open(image), hash_size=hash_size)
