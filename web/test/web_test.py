import cv2
import matplotlib.path as mpath

import numpy as np
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

def test1():
    img_src = cv2.imread('F:\code\pywork\\tianxian\img\\2077\\1\\2.jpg')
    x,y = img_src.shape[:2]
    img_src = cv2.resize(img_src, (int(y/2),int(x/2)))
    img = cv2.cvtColor(src=img_src, code=cv2.COLOR_BGR2GRAY)
    for i in range(255):
        ret, img_binary = cv2.threshold(src=img, thresh=i, maxval=255, type=cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image=img_binary, mode=cv2.CHAIN_APPROX_NONE,
                                               method=cv2.CHAIN_APPROX_SIMPLE)
        image = cv2.drawContours(image=img_src, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1)
        cv2.imshow("img", img_binary)
        print(i)
        cv2.waitKey(0)
    # for item in range(len(contours)):
    #     img = cv2.drawContours(image=img_src, contours=contours, contourIdx=item, color=(0, 255, 0), thickness=1)
    #     print(item)
    #     cv2.imshow("img", img)
    #     cv2.waitKey(0)
    cv2.destroyAllWindows()


def FindContours(img_path='images/external.png'):
    # 读取图像
    img_src = cv2.imread(img_path)
    img_src = cv2.resize(src=img_src, dsize=(450, 450))
    # 图像灰度化
    img = cv2.cvtColor(src=img_src, code=cv2.COLOR_BGR2GRAY)
    # print(img.shape)
    # 图像二值化
    ret, img_binary = cv2.threshold(src=img, thresh=150, maxval=255, type=cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=img_binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    # 打印出轮廓列表
    print("contours: {}".format(contours))
    # 绘制轮廓
    dst = cv2.drawContours(image=img_src, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1)

    # 显示图片
    # cv2.imshow('img_src',img_src)
    cv2.imshow('dst', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def gaolian():
    img = cv2.imread('F:\code\pywork\\tianxian\img\\2077\\1\\1.jpg')
    img = cv2.resize(img, (540, 600))
    # 转换为灰度图像
    x, y, w, h = 100, 100, 200, 200

    # 绘制矩形框
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 将矩形内的像素值设置为最大值（255）
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    mask[y:y + h, x:x + w] = 1

    # 将掩码应用于原始图像，实现高亮显示
    result = cv2.bitwise_and(img, img, mask=mask)
    result[mask == 255] = [0, 255, 255]  # 将掩码中的白色（255）替换为原始图像中的白色（[255, 255, 255]）

    # 显示高亮图像
    cv2.imshow('image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def gaolian_1():
    image = cv2.imread('F:\code\pywork\\tianxian\img\\2077\\1\\2.jpg')
    image = cv2.resize(image, (540, 600))
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, img_binary = cv2.threshold(src=gray, thresh=150, maxval=255, type=cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=img_binary, mode=cv2.CHAIN_APPROX_TC89_L1,
                                           method=cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(image=image, contours=contours, contourIdx=17, color=(0, 255, 0), thickness=1)
    # 创建高亮图像
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    arr_list = []
    for item in contours[17]:
        arr_list.append((item[0][0],item[0][1]))
    P = np.array(arr_list)
    inside = []
    for point in mask:
        path = mpath.Path(arr_list, codes=None)
        print(path)
        if path.contains_point(point):
            inside.append(point)
    print(inside)
    # for item in contours[17]:
    #     arr_list.append((item[0][0],item[0][1]))
    # polygon = Polygon(arr_list)
    # x, y = img.shape[:2]
    # for item_x in range(x):
    #     for item_y in range(y):
    #         point = Point(item_x, item_y)
    #         contains = polygon.contains(point)
    #         if contains:
    #             mask[item_y,item_x] = 1
    #
    # result = cv2.bitwise_and(img, img, mask=mask)
    # result[mask == 255] = [0, 255, 255]  # 将掩码中的白色（255）替换为原始图像中的白色（[255, 255, 255]）

    # 显示高亮图像
    # cv2.imshow('image', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #
    # # 合并高亮图像与原始图像的不规则区域部分

    # 显示高亮图像
    # cv2.imshow('image', contour_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def ganlian_2():
    pic = cv2.imread('F:\code\pywork\\tianxian\img\\2077\\1\\1.jpg')
    pic = cv2.resize(pic, dsize=(500, 400), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 5)
    _, thres = cv2.threshold(blur, 100, 250, cv2.THRESH_TOZERO)
    res = cv2.Canny(thres, 100, 250, L2gradient=True)

    circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, 1, 20, param1=200, param2=15, minRadius=80, maxRadius=100)
    circles = np.uint16(np.around(circles))

    mask = np.full((res.shape[0], res.shape[1]), 1, dtype=np.uint8)  # mask is only
    clone = pic.copy()
    for i in circles[0, :]:
        cv2.circle(mask, (i[0], i[1]), i[2], (255, 255, 255), -1)
        cv2.circle(clone, (i[0], i[1]), i[2], (255, 255, 255), 1)

    # get first masked value (foreground)
    fg = cv2.bitwise_or(res, res, mask=mask)

    # get second masked value (background) mask must be inverted
    mask = cv2.bitwise_not(mask)
    background = np.full(res.shape, 255, dtype=np.uint8)
    bk = cv2.bitwise_or(background, background, mask=mask)

    # combine foreground+background
    final = cv2.bitwise_or(fg, bk)

    result = np.concatenate((res, final), axis=1)
    cv2.imshow('Hole', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ganlian_3():
    img_src = cv2.imread('F:\code\pywork\\tianxian\img\\2077\\1\\1.jpg')
    img_src = cv2.resize(img_src, (540, 600))
    img = cv2.cvtColor(src=img_src, code=cv2.COLOR_BGR2GRAY)
    ret, img_binary = cv2.threshold(src=img, thresh=150, maxval=255, type=cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(image=img_binary, mode=cv2.CHAIN_APPROX_TC89_L1,
                                           method=cv2.CHAIN_APPROX_SIMPLE)
    contours_ = contours[17]
    print(contours_)
    img = cv2.drawContours(image=img_src, contours=contours, contourIdx=17, color=(0, 255, 0), thickness=1)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # FindContours('F:\code\pywork\\tianxian\img\\2077\\1\\1.jpg')
    gaolian_1()
    pass
