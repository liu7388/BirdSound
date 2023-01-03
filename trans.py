from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import os
import wave
from wave import Wave_read


def cut_and_trans(k, audio, path2):
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


def calculate(j, name_1):
    # 設定路徑
    path1 = './data/audio/' + name_1 + "/" + name_1 + str(j)  # 音檔所在位置
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


name1 = []

# 設定路徑
path = './data/鳥類.txt'

# 開啟鳥類txt檔
with open(path, 'r', encoding='utf-8') as f:
    # 逐行讀取txt檔
    for line in f.readlines():
        # 分割出鳥類名稱並將其存至list中
        s = line.split(' ')
        name1.append(s[0])

# 重複四次，代表四種鳥類
for i in range(0, 4):

    # 顯示目前正在轉換的鳥類種類
    name_1 = str(name1[i])
    print(name_1)

    # 設定音檔路徑
    path = "./data/audio/" + name_1
    n = len(os.listdir(path))  # n為該路徑中有幾個音檔

    # 將資料夾中的每個音檔都進行轉換
    for j in range(1, n):

        count, audio, path2 = calculate(j, name_1)  # 將指定參數匯入calculate函式並獲取新的值

        if int(count) > 0:
            # 如果calculate函數計算後所得的count>0，也就是該音檔可以被10整除
            for k in range(0, int(count)):
                # 執行音檔切分並轉換為圖檔
                cut_and_trans(k, audio, path2)

        else:
            # 其他便是音檔過短的情形
            print('音檔過短')
            pass

# https://docs.python.org/zh-cn/3/library/wave.html
# https://www.twblogs.net/a/5c1fabb8bd9eee16b3dab5d6
