from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp
import os
import wave
from wave import Wave_read

name1 = []

path = './data/鳥類.txt'

with open(path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        s = line.split(' ')
        name1.append(s[0])

for i in range(0, 3):
    m = 1
    name_1 = str(name1[i])
    print(name_1)

    path = "./data/audio/" + name_1
    n = len(os.listdir(path))

    for j in range(1, n):
        path1 = './data/audio/' + name_1 + "/" + name_1 + str(j)
        path2 = './data/images/' + name_1

        print(name_1 + str(j))

        if os.path.exists(path2):
            pass
        else:
            os.mkdir(path2)

        audio = AudioSegment.from_file(path1 + '.mp3', format="mp3")
        wname = mktemp('.wav')  # 暫存資料夾
        audio1 = audio.export(wname, format="wav")  # 轉換成 wav
        file = wave.open(audio1, 'r')
        a = Wave_read.getnframes(file)
        f = Wave_read.getframerate(file)  # 採樣頻率
        time = a / f
        print(time)
        count = time / 10
        print(int(count))

        if int(count) > 0:
            for k in range(0, int(count)):
                audio[k * 1000:(k + 1) * 1000].export('output.mp3')  # 取出 1500 毫秒～5500 毫秒長度的聲音，輸出為 output.mp3
                audio2 = AudioSegment.from_file('output.mp3', format="mp3")
                wname = mktemp('.wav')  # 暫存資料夾
                audio2.export(wname, format="wav")  # 轉換成 wav
                FS, data = wavfile.read(wname)
                # print(data)
                try:
                    plt.specgram(data[:, 0], Fs=FS)  # 畫圖
                    plt.ylabel('Frequency [Hz]')
                    plt.xlabel('Time')
                    plt.savefig(path2 + '/' + name_1 + str(m) + '.png')
                    # plt.show()
                    m += 1
                except IndexError:
                    # os.remove(path1 + '.mp3')
                    pass
        else:
            print('音檔過短')
            pass

# https://docs.python.org/zh-cn/3/library/wave.html
# https://www.twblogs.net/a/5c1fabb8bd9eee16b3dab5d6
