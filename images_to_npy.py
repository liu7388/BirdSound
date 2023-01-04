import random
from tqdm import tqdm
from library import *

m = 0


def image_label(imageLabel, label2idx, i):
    """返回图片的label
    """
    if imageLabel not in label2idx:
        label2idx[imageLabel] = i
        i = i + 1
    # 返回的是字典类型
    return label2idx, i


def check():
    path = './data/label/'

    for img_file in os.listdir(path):
        if '.npy' in img_file:
            os.remove('./data/label/' + img_file)
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
    np.save('./data/label/train-images-idx3.npy', X_train)
    np.save('./data/label/train-labels-idx1.npy', y_train)
    np.save('./data/label/t10k-images-idx3.npy', X_test)
    np.save('./data/label/t10k-labels-idx1.npy', y_test)
    return label2idx


check()
image2npy('./data/label/', 0.2)

