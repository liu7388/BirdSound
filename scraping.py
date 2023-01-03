import requests
from bs4 import BeautifulSoup
import os


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
            with open(file=path + name3 + '0' + title + '.mp3', mode='wb') as f:
                f.write((res.content))  # 下載MP3到指定位置，並命名為指定的名稱
                print(name3 + '0' + title + '.mp3' + "下載成功")

    except IndexError:
        print("本頁下載成功")
        # 如果index裡沒有資料了，就代表載完了全部的音檔


def page(i, name):
    try:
        for j in range(1, 100):
            url = "https://xeno-canto.org/species/" + str(name) + "?pg=" + str(j)  # 透過for迴圈抓取不同頁的資料
            print(url)  # 印出當前頁面的網址
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")  # 獲取網頁的HTML
            container = soup.findAll("audio", class_="xc-mini-player")  # 透過audio標籤及class，獲取MP3的檔案路徑
            catch_audio(i=i, j=j, name=name1, path=path1, container=container)  # 呼叫catch_audio函式
    except:
        # 遇到其他錯誤的話即pass
        pass


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
    path1 = './data/audio/' + name_1 + '/'
    if os.path.exists(path1):
        # 如果資料夾存在，則pass
        pass
    else:
        # 如果資料夾不存在，建立一個資料夾，名稱為name_1
        os.mkdir(path1)

    # 整理爬蟲之鳥類名稱
    name_2 = name2[i].replace("\n", "")
    print(name_2)

    try:
        page(i, name_2)  # 執行page函式
        print(str(name_2) + "下載成功")  # 下載完了整頁的音檔

    except IndexError:
        print('下載完成')
        # 如果index裡沒有資料了，就代表載完了全部的音檔
