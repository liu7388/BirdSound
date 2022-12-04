import requests
from bs4 import BeautifulSoup
import os


def catch_audio(i, j, name, path, container):
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
            name3 = str(name[i])
            with open(file=path + name3 + '0' + title + '.mp3', mode='wb') as f:
                f.write((res.content))  # 下載MP3到指定位置，並命名為指定的名稱
                print(name3 + '0' + title + '.mp3' + "下載成功")

    except IndexError:
        print("本頁完成下載")
        # 如果index裡沒有資料了，就代表載完了全部的音檔


def page(i, name):
    try:
        url = "https://xeno-canto.org/species/" + str(name) + "?pg=" + str(j)  # 透過for迴圈抓取不同頁的資料
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")  # 獲取網頁的HTML
        container = soup.findAll("audio", class_="xc-mini-player")  # 透過audio標籤及class，獲取MP3的檔案路徑
        catch_audio(i=i, j=j, name=name1, path=path1, container=container)
    except IndexError:
        print(str(name) + "完成下載")


name1 = []
name2 = []

path = 'C:/Users/asus/OneDrive - 國立臺北科技大學/鳥類資料/'

with open(path + '鳥類01.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        s = line.split(' ')
        name1.append(s[0])
        name2.append(s[1])
# print(name1)
# print(name2)

for i in range(0, 4):
    name3 = str(name1[i])
    path1 = path + name3 + '//'
    if os.path.exists(path1):
        pass
    else:
        os.mkdir(path1)
    name = name2[i].replace("\n", "")
    print(name)
    for j in range(1, 500):
        page(i=i, name=name)
