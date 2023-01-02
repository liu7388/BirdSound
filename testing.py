import os
import random
from tqdm import tqdm

dir_path = './data/images/'
labels = ['Anas', 'Hirun', 'Motac', 'Passer']
num = []

for i in labels:
    num.append(len([name for name in os.listdir(dir_path + i) if os.path.isfile(os.path.join(dir_path + i, name))]))

number = min(num)

