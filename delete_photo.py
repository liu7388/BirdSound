from tqdm import tqdm
from library import *

"""
此檔案透過圖檔與目標圖檔的對比(目標圖檔為人工篩選)
刪去一些對於深度學習沒有用的圖片資料
例如無鳥叫聲的空白圖檔等
"""

# 設定路徑與預設值
dir_path = './data/label/'
labels = ['Anas', 'Hirun', 'Motac', 'Passer']

# 在四種鳥類中
for i in range(0, 4):
    # 獲得鳥名
    for j in labels:
        for (root, dirs, files) in os.walk(dir_path + str(j)):
            for Ufile in tqdm(files):
                try:
                    img_path = os.path.join(root, Ufile)  # 獲得圖檔路徑(待比對)
                    sensitive_pic = im_read(img_path)  # 讀取圖片
                    sensitive_pic = gray_img(sensitive_pic)  # 將圖片灰階化
                    target_path = './data/images/target/target' + str(i) + '.png'  # 獲得圖檔路徑(目標圖檔)
                    target_pic = im_read(target_path)  # 讀取圖片
                    target_pic = gray_img(target_pic)  # 將圖片灰階化
                    compare_images(sensitive_pic, target_pic, img_path)  # 比對圖片並依需要刪除圖檔
                # 如檔案不存在則pass
                except FileNotFoundError:
                    pass
