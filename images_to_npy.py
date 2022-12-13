import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm

path = "./"
save_path = "C:/Users/asus/OneDrive/桌面/功課/111-1/深度學習/pythonProject/"
print(os.listdir(path))
m = 0


def im_read(img_file):
    img_file = cv2.imdecode(np.fromfile(img_file, dtype=np.uint8), -1)
    return img_file


def im_write(save_path, m, name):
    cv2.imencode('.jpg', name)[1].tofile(save_path + str(m) + '.jpg')


def show_img(img):
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()


def crop_img(img):
    # x_l, x_r = 80, 576  # left, right
    # y_u, y_d = 58, 427  # up, down

    x_l, x_r = 80, 576  # left, right
    y_u, y_d = 58, 411  # up, down
    crop = img[y_u:y_d, x_l:x_r]  # notice: first y, then x
    return crop


def HSV_img(img):
    redhsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return redhsv1


def gray_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def white_noise(image, min_noise, max_noise):
    img = np.copy(image)
    noise = np.random.randint(min_noise, max_noise, img.shape)
    return np.clip(img + noise, 0, 255).astype('uint8')


def gaussian_noise(image, mean=0, sigma=1):
    img = np.copy(image)
    noise = np.random.normal(mean, sigma, img.shape)
    return np.clip(img + noise, 0, 255).astype('uint8')


def salt_pepper_noise(image, fraction, salt_vs_pepper):
    img = np.copy(image)
    size = img.size
    num_salt = np.ceil(fraction * size * salt_vs_pepper).astype('int')
    num_pepper = np.ceil(fraction * size * (1 - salt_vs_pepper)).astype('int')
    row, column = img.shape

    x = np.random.randint(0, column - 1, num_pepper)
    y = np.random.randint(0, row - 1, num_pepper)
    img[y, x] = 0

    x = np.random.randint(0, column - 1, num_salt)
    y = np.random.randint(0, row - 1, num_salt)
    img[y, x] = 255
    return img


def image_label(imageLabel, label2idx, i):
    """返回图片的label
    """
    if imageLabel not in label2idx:
        label2idx[imageLabel] = i
        i = i + 1
    # 返回的是字典类型
    return label2idx, i


def check():
    path = './label/'

    for img_file in os.listdir(path):
        if '.npy' in img_file:
            os.remove('./label/' + img_file)
        else:
            pass


def image2npy(dir_path, testScale):
    """生成npy文件
    """
    i = 0
    label2idx = {}
    data = []
    for (root, dirs, files) in os.walk(dir_path):
        for Ufile in tqdm(files):
            # Ufile是文件名
            img_path = os.path.join(root, Ufile)  # 文件的所在路径
            File = root.split('/')[-1]  # 文件所在文件夹的名字, 也就是label
            img = im_read(img_path)
            crop_im = crop_img(img)
            gray = gray_img(crop_im)
            image = cv2.GaussianBlur(white_noise(gray, -5, 5), (3, 3), 15)
            img_data = cv2.resize(image, (45, 21), interpolation=cv2.INTER_CUBIC)

            label2idx, i = image_label(File, label2idx, i)
            label = label2idx[File]

            # 存储image和label数据
            data.append([np.array(img_data), label])

    random.shuffle(data)  # 随机打乱,直接打乱data
    # 训练集和测试集的划分
    testNum = int(len(data) * testScale)
    train_data = data[:-1 * testNum]  # 训练集
    test_data = data[-1 * testNum:]  # 测试集
    # 测试集的输入输出和训练集的输入输出
    X_train = np.array([i[0] for i in train_data], dtype=object)  # 训练集特征
    y_train = np.array([i[1] for i in train_data], dtype=object)  # 训练集标签
    X_test = np.array([i[0] for i in test_data], dtype=object)  # 测试集特征
    y_test = np.array([i[1] for i in test_data], dtype=object)  # 测试集标签
    print(len(X_train), len(y_train), len(X_test), len(y_test))
    # 保存文件
    np.save('./label/train-images-idx3.npy', X_train)
    np.save('./label/train-labels-idx1.npy', y_train)
    np.save('./label/t10k-images-idx3.npy', X_test)
    np.save('./label/t10k-labels-idx1.npy', y_test)
    return label2idx


check()
image2npy('./label/', 0.2)

image_no = np.random.randint(0, 15, size=2)  # 随机挑选9个数字
train_images = np.load('./label/train-images-idx3.npy', allow_pickle=True)
test_images = np.load('./label/t10k-images-idx3.npy', allow_pickle=True)
train_labels = np.load('./label/train-labels-idx1.npy', allow_pickle=True)
test_labels = np.load('./label/t10k-labels-idx1.npy', allow_pickle=True)
print(train_labels)

for i in range(0, 14):
    img = 255 * np.array(train_images[i]).astype('uint8')
    im_write('./', i, np.array(img))
    np.set_printoptions(threshold=np.inf)
    print(np.array(img))
    print(i, train_labels[i])

for i in range(0, 1):
    img = 255 * np.array(test_images[i]).astype('uint8')
    im_write('./', i, np.array(img))
    print(i, test_labels)