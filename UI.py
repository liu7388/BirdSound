import tkinter as tk
from tkinter import filedialog
from library import *
import pyaudio
import wave
import sys
from PIL import Image, ImageTk


def show():
    file_path = filedialog.askopenfilename()  # 選擇檔案後回傳檔案路徑與名稱
    print(file_path)  # 印出路徑
    predict(file_path)


def predict(file_path):
    path = './data/images/test'
    count, audio = calc(1, 'test', file_path, path)
    if int(count) > 0:
        # 如果calculate函數計算後所得的count>0，也就是該音檔可以被10整除
        cut_and_trans(1, audio, path, 'test')  # 執行音檔切分並轉換為圖檔
    else:
        print('音檔過短')
        sys.exit()

    img_path = './data/images/test/test1.png'
    img = Image.open(img_path)  # 取得圖片路徑
    w, h = img.size  # 取得圖片長寬
    tk_img = ImageTk.PhotoImage(img)  # 轉換成 tk 圖片物件
    canvas.delete('all')  # 清空 Canvas 原本內容
    canvas.config(scrollregion=(0, 0, w, h))  # 改變捲動區域
    canvas.create_image(0, 0, anchor='nw', image=tk_img)  # 建立圖片
    canvas.tk_img = tk_img  # 修改屬性更新畫面


def record():
    chunk = 1024  # 記錄聲音的樣本區塊大小
    sample_format = pyaudio.paInt16  # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
    channels = 2  # 聲道數量
    fs = 44100  # 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
    seconds = 11  # 錄音秒數
    filename = "test.wav"  # 錄音檔名

    p = pyaudio.PyAudio()  # 建立 pyaudio 物件

    root1 = tk.Tk()
    root1.title('Recording')
    root1.configure(background='#a9b4c2')
    width = 800
    height = 600
    left = int((window_width - width) / 2)  # 計算左上 x 座標
    top = int((window_height - height) / 2)  # 計算左上 y 座標
    root1.geometry(f'{width}x{height}+{left}+{top}')

    # tk.Label(text='Start recording!', fg='#a9b4c2', bg='#eef1ef', width=20, height=1, font=('times', 24)).pack()

    print("開始錄音...")

    # 開啟錄音串流
    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

    frames = []  # 建立聲音串列

    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)  # 將聲音記錄到串列中

    stream.stop_stream()  # 停止錄音
    stream.close()  # 關閉串流
    p.terminate()

    print('錄音結束...')
    # tk.Label(text='Finish recording!', fg='#a9b4c2', bg='#eef1ef', width=20, height=1, font=('times', 24)).pack()

    wf = wave.open(filename, 'wb')  # 開啟聲音記錄檔
    wf.setnchannels(channels)  # 設定聲道
    wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
    wf.setframerate(fs)  # 設定取樣頻率
    wf.writeframes(b'./'.join(frames))  # 存檔
    wf.close()

    file_path = './test.wav'
    predict(file_path)


root = tk.Tk()

root.title('BirdSound')

window_width = root.winfo_screenwidth()  # 取得螢幕寬度
window_height = root.winfo_screenheight()  # 取得螢幕高度
root.configure(background='#a9b4c2')

width = 800
height = 600
left = int((window_width - width) / 2)  # 計算左上 x 座標
top = int((window_height - height) / 2)  # 計算左上 y 座標
root.geometry(f'{width}x{height}+{left}+{top}')

root.resizable(False, False)  # 視窗不可縮放

tk.Label(text='Welcome to BirdSound!', fg='#a9b4c2', bg='#eef1ef', width=20, height=1, font=('times', 24)).place(x=230,
                                                                                                                 y=30)

# Button 設定 command 參數，點擊按鈕時執行 show 函式
tk.Button(root, text='Open file', command=show, width=10, height=1, bg='#eef1ef', font=('times', 8)).place(x=620,
                                                                                                           y=100)
tk.Button(root, text='Record', command=record, width=10, height=1, bg='#eef1ef', font=('times', 8)).place(x=120, y=100)

frame = tk.Frame(root, width=700, height=400)  # 放 Canvas 的 Frame
frame.place(x=50, y=150)

canvas = tk.Canvas(frame, width=700, height=400, bg='#fff')  # Canvas

scrollX = tk.Scrollbar(frame, orient='horizontal')  # 水平捲軸
scrollX.pack(side='bottom', fill='x')
scrollX.config(command=canvas.xview)

scrollY = tk.Scrollbar(frame, orient='vertical')  # 垂直捲軸
scrollY.pack(side='right', fill='y')
scrollY.config(command=canvas.yview)

canvas.config(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)  # Canvas 綁定捲軸
canvas.pack(side='left')

root.mainloop()
