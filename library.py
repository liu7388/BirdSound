from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import wave
from wave import Wave_read
import numpy as np
import cv2
import requests
from bs4 import BeautifulSoup
import os
import sys


# 音檔轉圖檔
def cut_and_trans(k, audio, image_path, name_1):
    m = 1

    audio[k * 1000:(k + 1) * 1000].export('output.wav')
    audio2 = AudioSegment.from_file('output.mp3', format="mp3")  # 讀取output.mp3
    wname = mktemp('.wav')  # 暫存資料夾
    audio2.export(wname, format="wav")  # 轉換成 wav

    FS, data = wavfile.read(wname)  # 從wav中讀出取樣頻率與取樣數據

    try:
        # 嘗試畫圖並存成png檔
        plt.specgram(data[:, 0], Fs=FS)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time')
        plt.savefig(image_path + '/' + name_1 + str(m) + '.png')
        m += 1

    except IndexError:
        pass  # 如果出現Index沒有資料了，則pass


def calc(j, name_1, audio_path, path):
    # 印出正在計算&轉換的檔名
    print(name_1 + str(j))

    if os.path.exists(path):
        # 如果資料夾存在，則pass
        pass
    else:
        os.mkdir(path)
        # 如果資料夾不存在，建立一個資料夾，名稱為name_1

    if '.mp3' in audio_path:
        audio = AudioSegment.from_file(audio_path, format="mp3")  # 開啟mp3檔
        wname = mktemp('.wav')  # 暫存資料夾
        audio1 = audio.export(wname, format="wav")  # 轉換成 wav
        # 使用wave打開wav音檔

    elif '.wav' in audio_path:
        audio = AudioSegment.from_file(audio_path, format="wav")
        wname = mktemp('.wav')
        audio.export(wname, format("mp3"))
        audio1 = audio.export(wname, format="wav")

    else:
        print('不支援此檔案格式')
        sys.exit()

    file = wave.open(audio1, 'r')

    a = Wave_read.getnframes(file)  # 音頻總幀數
    f = Wave_read.getframerate(file)  # 採樣頻率
    # 總幀數除以採樣頻率得到秒數
    time = a / f
    print(time)

    # 每十秒切分，得到切分數量
    count = time / 10
    print(int(count))

    return count, audio


# 處理圖片
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


# 比較兩張圖片相似度
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


# 爬蟲
def catch_audio(i, j, name, path, container):
    # 顯示現在正在下載的頁數
    print("現在正在下載第" + str(j) + '頁')
    try:
        for k in range(0, 100):
            container1 = container[k]['src']  # 特別抓出檔案的URL
            url1 = "https:" + container1  # 完善URL
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
            # 自訂 Header，避免被網站擋掉
            res = requests.get(url=url1, headers=headers)
            title = str((j - 1) * 30 + k + 1)  # 幫檔案編碼
            name3 = str(name[i])  # 欲儲存的檔名
            with open(file=path + name3 + title + '.mp3', mode='wb') as f:
                f.write((res.content))  # 下載MP3到指定位置，並命名為指定的名稱
                print(name3 + title + '.mp3' + "下載成功")

    except IndexError:
        print("本頁下載成功")
        # 如果index裡沒有資料了，就代表載完了全部的音檔


def page(i, name, name1, audio_path):
    try:
        for j in range(1, 100):
            url = "https://xeno-canto.org/species/" + str(name) + "?pg=" + str(j)  # 透過for迴圈抓取不同頁的資料
            print(url)  # 印出當前頁面的網址
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")  # 獲取網頁的HTML
            container = soup.findAll("audio", class_="xc-mini-player")  # 透過audio標籤及class，獲取MP3的檔案路徑
            catch_audio(i=i, j=j, name=name1, path=audio_path, container=container)  # 呼叫catch_audio函式
    except:
        # 遇到其他錯誤的話即pass
        pass
