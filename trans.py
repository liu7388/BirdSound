from library import *

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
        audio_path = './data/audio/' + name_1 + "/" + name_1 + str(j)  # 音檔所在位置
        image_path = './data/images/' + name_1  # 圖檔儲存資料夾
        count, audio = calc(j, name_1, audio_path, image_path)  # 將指定參數匯入calc函式並獲取新的值

        if int(count) > 0:
            # 如果calculate函數計算後所得的count>0，也就是該音檔可以被10整除
            for k in range(0, int(count)):
                # 執行音檔切分並轉換為圖檔
                cut_and_trans(k, audio, image_path, name_1)

        else:
            # 其他便是音檔過短的情形
            print('音檔過短')
            pass
