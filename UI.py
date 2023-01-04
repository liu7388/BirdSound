import tkinter as tk
from tkinter import filedialog
from trans import *

root = tk.Tk()

root.title('oxxo.studio')

window_width = root.winfo_screenwidth()  # 取得螢幕寬度
window_height = root.winfo_screenheight()  # 取得螢幕高度

width = 600
height = 400
left = int((window_width - width) / 2)  # 計算左上 x 座標
top = int((window_height - height) / 2)  # 計算左上 y 座標
root.geometry(f'{width}x{height}+{left}+{top}')

tk.Label(text='Welcome to BirdSound!').pack()


def show():
    file_path = filedialog.askopenfilename()  # 選擇檔案後回傳檔案路徑與名稱
    print(file_path)  # 印出路徑
    count, audio, path2 = calculate(1, "test", file_path)
    if int(count) > 0:
        # 如果calculate函數計算後所得的count>0，也就是該音檔可以被10整除
        # 執行音檔切分並轉換為圖檔
        cut_and_trans(1, audio, path2, "test")
    else:
        print('音檔過短')


# Button 設定 command 參數，點擊按鈕時執行 show 函式
tk.Button(root, text='開啟檔案', command=show).pack()

root.mainloop()
