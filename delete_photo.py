import os
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2


def im_read(img_file):
    img_file = cv2.imdecode(np.fromfile(img_file, dtype=np.uint8), -1)
    return img_file


def gray_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def mse(imageA, imageB):
    # 計算兩張圖片的MSE指標
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # 返回結果，該值越小越好
    return err


def compare_images(imageA, imageB, img_path):
    # 計算輸入圖片的MSE指標值的大小
    m = mse(imageA, imageB)
    if m < 400:
        os.remove(img_path)
    else:
        pass
    # print("MSE: %.2f, SSIM: %.2f" % (m, s))


dir_path = './data/label/'
labels = ['Anas', 'Hirun', 'Motac', 'Passer']

for i in range(1, 4):
    for j in labels:
        for (root, dirs, files) in os.walk(dir_path + str(j)):
            for Ufile in tqdm(files):
                try:
                    img_path = os.path.join(root, Ufile)
                    sensitive_pic = im_read(img_path)
                    sensitive_pic = gray_img(sensitive_pic)
                    target_path = './data/images/target/target' + str(i) + '.png'
                    target_pic = im_read(target_path)
                    target_pic = gray_img(target_pic)
                    compare_images(sensitive_pic, target_pic, img_path)
                except FileNotFoundError:
                    pass
