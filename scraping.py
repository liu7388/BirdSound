from library import *

name1 = []
name2 = []

# 設定路徑
path = './data/鳥類.txt'

# 開啟鳥類txt檔
with open(path, 'r', encoding='utf-8') as f:
    # 逐行讀取txt檔
    for line in f.readlines():
        # 分割出鳥類名稱並將其存至list中
        s = line.split(' ')
        name1.append(s[0])  # 資料夾儲存名稱
        name2.append(s[1])  # 爬蟲url所需名稱

# 重複四次，代表四種鳥類
for i in range(0, 4):
    # 顯示目前正在下載的鳥類種類
    name_1 = str(name1[i])

    # 設定音檔路徑
    audio_path = './data/audio/' + name_1 + '/'
    if os.path.exists(audio_path):
        # 如果資料夾存在，則pass
        pass
    else:
        # 如果資料夾不存在，建立一個資料夾，名稱為name_1
        os.mkdir(audio_path)

    # 整理爬蟲之鳥類名稱
    name_2 = name2[i].replace("\n", "")
    print(name_2)

    try:
        page(i, name_2, name1, audio_path)  # 執行page函式
        print(str(name_2) + "下載成功")  # 下載完了整頁的音檔

    except IndexError:
        print('下載完成')
        # 如果index裡沒有資料了，就代表載完了全部的音檔
