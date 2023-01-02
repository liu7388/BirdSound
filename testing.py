import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from PIL.Image import Resampling
from tqdm import tqdm
from functools import reduce
from PIL import Image

import numpy as np
import cv2
import matplotlib.pyplot as plt


def histogram(f):
    if f.ndim != 3:
        hist = cv2.calHist([f], [0], None, [256], [0, 256])
        # plt.plot(hist)
    else:
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist(f, [i], None, [256], [0, 256])
            # plt.plot(hist, color = col)
    # plt.xlim([0, 256])
    # plt.xlabel("Intensity")
    # plt.ylabel("#Intensities")
    # plt.show()


m = 0


def im_read(img_file):
    img_file = cv2.imdecode(np.fromfile(img_file, dtype=np.uint8), -1)
    return img_file


def show_img(img):
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()


def crop_img(img):
    # x_l, x_r = 80, 576  # left, right
    # y_u, y_d = 58, 427  # up, down

    x_l, x_r = 80, 576  # left, right
    y_u, y_d = 58, 386  # up, down
    crop = img[y_u:y_d, x_l:x_r]  # notice: first y, then x
    return crop


def gray_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


"""

dir_path='./data/images/Anas1'
for (root, dirs, files) in os.walk(dir_path):
    for Ufile in tqdm(files):
        img_path = os.path.join(root, Ufile)
        # print(img_path)
        img = im_read(img_path)
        crop = crop_img(img)
        ROI = crop
        histogram(ROI)
        # print("Sigma = ", np.std(ROI))
        if np.std(ROI) < 75.3:
            os.remove(img_path)
        else:
            pass
        """

"""
# 計算圖片的局部哈希值--pHash
def phash(img):
    
    # param img: 圖片
    # return: 返回圖片的局部hash值
   
    img = img.resize((8, 8), Resampling.LANCZOS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    hash_value = reduce(lambda x, y: x | (y[1] << y[0]), enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),
                        0)
    print(hash_value)
    return hash_value


# 計算漢明距離:
def hamming_distance(a, b):
   
    # :param a: 圖片1的hash值
    # :param b: 圖片2的hash值
    # :return: 返回兩個圖片hash值的漢明距離
   
    hm_distance = bin(a ^ b).count('1')
    print(hm_distance)
    return hm_distance


# 計算兩個圖片是否相似:
def is_imgs_similar(img1, img2):
    
    # :param img1: 圖片1
    # :param img2: 圖片2
    # :return:  True 圖片相似  False 圖片不相似
    
    # return True if hamming_distance(phash(img1), phash(img2)) < 1 else False

dir_path = './data/images/Anas2'
for (root, dirs, files) in os.walk(dir_path):
    for Ufile in tqdm(files):
        img_path = os.path.join(root, Ufile)
        print(img_path)
        sensitive_pic = Image.open(img_path)
        target_path = './data/images/target/Anas8.png'
        target_pic = Image.open(target_path)
        result = is_imgs_similar(target_pic, sensitive_pic)"""

"""
dir_path = './data/images/Anas2'
target = {5, 8, 54, 310}
for i in target:
    for (root, dirs, files) in os.walk(dir_path):
        for Ufile in tqdm(files):
            img_path = os.path.join(root, Ufile)
            sensitive_pic = Image.open(img_path)
            target_path = './data/images/target/Anas' + str(i) + '.png'
            target_pic = Image.open(target_path)

            result = is_imgs_similar(target_pic, sensitive_pic)

            if result:
                os.remove(img_path)
            else:
                pass
"""

from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2


def mse(imageA, imageB):
    # 計算兩張圖片的MSE指標
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # 返回結果，該值越小越好
    return err


def compare_images(imageA, imageB, img_path):
    # 分別計算輸入圖片的MSE和SSIM指標值的大小
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    if m < 400:
        os.remove(img_path)
    else:
        pass
    # print("MSE: %.2f, SSIM: %.2f" % (m, s))


dir_path = './data/images/Anas2'
target = {5, 8, 54, 310}
for i in target:
    for (root, dirs, files) in os.walk(dir_path):
        for Ufile in tqdm(files):
            img_path = os.path.join(root, Ufile)
            sensitive_pic = im_read(img_path)
            sensitive_pic = gray_img(sensitive_pic)
            target_path = './data/images/target/Anas' + str(i) + '.png'
            target_pic = im_read(target_path)
            target_pic = gray_img(target_pic)
            compare_images(sensitive_pic, target_pic, img_path)
