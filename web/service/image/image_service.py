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

    def cropping(self, x, x1, y, y1):
        # 图片裁剪
        image = self.file_model.image_file_buff
        image = cv2.imread(image)
        return image[x:y, x1:y1]

    def img_zip(self, x):
        #图片压缩
        image = self.file_model.image_file_buff
        image = cv2.imread(image)
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, x]
        compressed_image, _ = cv2.imencode('.jpg', image, compression_params)
        return compressed_image

    def adjust_exposure(self,image, gamma):
        #曝光
        adjusted = cv2.pow(image / 255.0, gamma)
        return adjusted

    def adjust_clarity(self,image, amount):
        # 调整鲜明度
        blurred = cv2.GaussianBlur(image, (0, 0), amount)
        sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
        return sharpened

    def adjust_highlight(self,image, alpha, beta):
        # 调整高光
        adjusted = cv2.addWeighted(image, alpha, image, 0, beta)
        return adjusted

    def adjust_shadow(self,image, alpha, beta):
        # 调整阴影
        adjusted = cv2.addWeighted(image, alpha, image, 0, beta)
        return adjusted

    def adjust_contrast(self,image, alpha):
        # 调整对比度为
        adjusted = cv2.convertScaleAbs(image, alpha=alpha)
        return adjusted

    def adjust_brightness(self,image, beta):
        # 调整亮度
        adjusted = np.clip(image + beta, 0, 255).astype(np.uint8)
        return adjusted

    def adjust_black_point(self,image, threshold):
        # 以灰度图像方式读取
        # 调整黑点
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        adjusted = cv2.bitwise_and(image, binary)
        return adjusted

    def adjust_saturation(self,image, alpha):
        # 调整饱和度
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        s = cv2.addWeighted(s, alpha, s, 0, 0)
        s = np.clip(s, 0, 255).astype(np.uint8)
        hsv_adjusted = cv2.merge([h, s, v])
        adjusted = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2BGR)
        return adjusted

    def adjust_natural_saturation(self,image, alpha):
        # 调整自然饱和度为100
        # 以灰度图像方式读取
        _, max_value, _, _ = cv2.minMaxLoc(image)
        adjusted = cv2.convertScaleAbs(image, alpha=alpha / max_value)
        return adjusted

    def adjust_white_balance(self,image, temperature):
        # 调整色温为5000
        kelvin_matrix = np.array([[temperature / 100, 0, 0],
                                  [0, temperature / 100, 0],
                                  [0, 0, temperature / 100]], dtype=np.float32)
        adjusted = cv2.transform(image, kelvin_matrix)
        return adjusted

    def adjust_hue(self,image, hue_shift):
        # 调整色调偏移量为20
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        h = cv2.add(h, hue_shift)
        h = np.clip(h, 0, 179).astype(np.uint8)
        hsv_adjusted = cv2.merge([h, s, v])
        adjusted = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2BGR)
        return adjusted

    def adjust_sharpness(self,image, amount):
        # 调整锐度为0.5
        blurred = cv2.GaussianBlur(image, (0, 0), 3 * amount)
        sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
        return sharpened

    def adjust_clarity(self,image, amount):
        # 调整清晰度
        blurred = cv2.GaussianBlur(image, (0, 0), amount)
        adjusted = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
        return adjusted

    def denoise(self,image):
        # 噪点消除
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        return denoised

    def adjust_vignette(self,image, sigma):
        # 调整晕影效果
        height, width = image.shape[:2]
        X, Y = np.meshgrid(np.linspace(-1, 1, width), np.linspace(-1, 1, height))
        D_squared = X ** 2 + Y ** 2
        vignette = np.exp(-D_squared / (2 * sigma ** 2))
        adjusted = cv2.multiply(image, vignette)
        return adjusted

    def image_similarity(self):
        # 计算图片相识度
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
        # 图片叠加
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
