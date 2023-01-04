from tqdm import tqdm
from library import *

dir_path = './data/label/'
labels = ['Anas', 'Hirun', 'Motac', 'Passer']

for i in range(1, 4):
    for j in labels:
        for (root, dirs, files) in os.walk(dir_path + str(j)):
            for Ufile in tqdm(files):
                try:
                    img_path = os.path.join(root, Ufile)
                    sensitive_pic = im_read(img_path)
                    sensitive_pic = gray_img(sensitive_pic)
                    target_path = './data/images/target/target' + str(i) + '.png'
                    target_pic = im_read(target_path)
                    target_pic = gray_img(target_pic)
                    compare_images(sensitive_pic, target_pic, img_path)
                except FileNotFoundError:
                    pass
