from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import os
import wave
from wave import Wave_read
import numpy as np
import cv2

def cut_and_trans(k, audio, path2, name_1):
    m = 1
    audio[k * 1000:(k + 1) * 1000].export('output.mp3')  # 將音檔切分，每1000毫秒切一次，並輸出為 output.mp3
    audio2 = AudioSegment.from_file('output.mp3', format="mp3")  # 讀取output.mp3
    wname = mktemp('.wav')  # 暫存資料夾
    audio2.export(wname, format="wav")  # 轉換成 wav
    FS, data = wavfile.read(wname)  # 從wav中讀出取樣頻率與取樣數據

    try:
        # 嘗試畫圖並存成png檔
        plt.specgram(data[:, 0], Fs=FS)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time')
        plt.savefig(path2 + '/' + name_1 + str(m) + '.png')
        m += 1

    except IndexError:
        pass  # 如果出現Index沒有資料了，則pass


def calculate(j, name_1, path1):
    # 設定路徑
    path2 = './data/images/' + name_1  # 圖檔儲存資料夾

    # 印出正在計算&轉換的檔名
    print(name_1 + str(j))

    if os.path.exists(path2):
        # 如果資料夾存在，則pass
        pass
    else:
        os.mkdir(path2)
        # 如果資料夾不存在，建立一個資料夾，名稱為name_1

    audio = AudioSegment.from_file(path1 + '.mp3', format="mp3")  # 開啟mp3檔
    wname = mktemp('.wav')  # 暫存資料夾
    audio1 = audio.export(wname, format="wav")  # 轉換成 wav
    file = wave.open(audio1, 'r')  # 使用wave打開wav音檔
    a = Wave_read.getnframes(file)  # 音頻總幀數
    f = Wave_read.getframerate(file)  # 採樣頻率

    # 總幀數除以採樣頻率得到秒數
    time = a / f
    print(time)

    # 每十秒切分，得到切分數量
    count = time / 10
    print(int(count))
    return count, audio, path2

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