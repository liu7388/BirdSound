import random
from tqdm import tqdm
from library import *

"""
此檔案主要用於將圖檔轉為numpy
並且將其作資料預處理(二值化與高斯模糊)
再將其標標籤存入npy檔中
方便後續深度學習時
將資料直接匯入做使用
"""

m = 0


# 返回圖片的標籤
def image_label(imageLabel, training_label, i):
    if imageLabel not in training_label:
        training_label[imageLabel] = i
        i = i + 1

    return training_label, i  # 返回字典


# 確認在label中是否存有npy檔
def check():
    path = './data/label/'

    for img_file in os.listdir(path):
        if '.npy' in img_file:
            # 若label中有npy檔則刪除，保證資料不會與前次執行之殘餘資料混淆
            os.remove('./data/label/' + img_file)
        else:
            pass


# 生成npy文件並標標籤
def image_to_npy(dir_path, testScale):
    # 設定預設值
    i = 0
    training_label = {}
    data = []

    for (root, dirs, files) in os.walk(dir_path):
        for Ufile in tqdm(files):
            # Ufile是文件名
            img_path = os.path.join(root, Ufile)  # 文件的所在路径
            File = root.split('/')[-1]  # 文件所在資料夾的名字, 也就是label
            img = im_read(img_path)  # 讀取圖片
            crop_im = crop_img(img)  # 切割圖片至指定的尺寸
            gray = gray_img(crop_im)  # 將圖片灰階化
            image = cv2.GaussianBlur(white_noise(gray, -5, 5), (3, 3), 15)  # 將圖片做高斯模糊
            img_data = cv2.resize(image, (45, 21), interpolation=cv2.INTER_CUBIC)  # 將圖片轉至指定的尺寸

            training_label, i = image_label(File, training_label, i)  # 獲得標籤
            label = training_label[File]  # 依原資料夾定標籤

            # 將圖片與label一同存至data中
            data.append([np.array(img_data), label])

    random.shuffle(data)  # 隨機打亂data

    # 劃分測試集與訓練集
    testNum = int(len(data) * testScale)
    train_data = data[:-1 * testNum]  # 訓練集
    test_data = data[-1 * testNum:]  # 測試集

    # 测试集的输入输出和训练集的输入输出
    X_train = np.array([i[0] for i in train_data], dtype=object)  # 訓練集圖片numpy
    y_train = np.array([i[1] for i in train_data], dtype=object)  # 訓練集標籤
    X_test = np.array([i[0] for i in test_data], dtype=object)  # 測試集圖片numpy
    y_test = np.array([i[1] for i in test_data], dtype=object)  # 測試集標籤
    print(len(X_train), len(y_train), len(X_test), len(y_test))

    # 保存文件
    np.save('./data/label1/train-images-idx3.npy', X_train)
    np.save('./data/label1/train-labels-idx1.npy', y_train)
    np.save('./data/label1/t10k-images-idx3.npy', X_test)
    np.save('./data/label1/t10k-labels-idx1.npy', y_test)

    return training_label  # 回傳training_label


check()  # 確認label中是否有npy檔
traning_label = image_to_npy('./data/label/', 0.2)  # 生成npy於label中，測試集：訓練集=2:8
print(traning_label)
