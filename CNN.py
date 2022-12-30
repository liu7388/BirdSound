# 引入函式庫
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import numpy as np
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


# 建立卷積神經網路
"""
卷積層(基底32/卷積核3*3/激活relu)
池化層(池化窗口大小2*2)
卷積層(基底64/卷積核3*3/激活relu)
池化層(池化窗口大小2*2)
Dropout層(比率為0.5)
扁平層
全連接層(輸出1024/激活relu)
全連接層(輸出4/激活softmax)
"""

model1 = Sequential(name="Model")

# block 1
model1.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=(21, 45, 1), activation='relu', padding='same',
                 name='block_1_conv'))  # 接收圖片為45*21且為灰階(1)
model1.add(MaxPooling2D(pool_size=(2, 2), name='block_1_pool'))
# block 2
model1.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same', name='block_2_conv'))
model1.add(MaxPooling2D(pool_size=(2, 2), name='block_2_pool'))
model1.add(Dropout(0.5))
# 扁平層
model1.add(Flatten(name="flatten"))
# 全連階層
model1.add(Dense(1024, activation='relu', name="Dense_1"))
model1.add(Dense(4, activation='softmax', name="Dense_2"))  # 分四種鳥類

model1.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

print(model1.summary())

# 建立提早結束CALLBACK
# validation accuracy 三個執行週期沒改善就停止訓練
callback1 = [tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_accuracy')]

# 載入資料
train_images = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\train-images-idx3.npy',allow_pickle=True)
train_labels = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\train-labels-idx1.npy',allow_pickle=True)
test_images = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\t10k-images-idx3.npy',allow_pickle=True)
test_labels = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\t10k-labels-idx1.npy',allow_pickle=True)

# 資料前處理
train_images=train_images.astype('float32')/255  #把輸入的灰度值/255，使其在0與1間
test_images=test_images.astype('float32')/255
train_labels=to_categorical(train_labels)     #One Hot Encoding
test_labels=to_categorical(test_labels)
train_images = train_images.reshape(-1, 21, 45, 1)
test_images = test_images.reshape(-1, 21, 45, 1)

# 訓練階段
# 訓練資料/訓練標籤/疊代20次/每次訓練抓200個樣本/訓練提早結束/
model_history = model1.fit(train_images,train_labels,epochs=20, batch_size=200, callbacks=callback1, validation_data=(test_images, test_labels))

# 測試階段
train_loss,train_acc=model1.evaluate(train_images,train_labels)
test_loss,test_acc=model1.evaluate(test_images,test_labels)
print("\nTrain loss:", train_loss, "Train Accuracy:", train_acc)
print("Test loss", test_loss, "Test Accuracy:", test_acc)

# 輸出預測圖
# ACCURACY
plt.figure()
plt.plot(model_history.history['accuracy'],color='darkcyan')
plt.plot(model_history.history['val_accuracy'],color='coral')
plt.title("Model Accuracy")
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(["train accuracy",'test accuracy'], loc='lower right')
plt.show()
# LOSS
plt.figure()
plt.plot(model_history.history['loss'], color='darkcyan')
plt.plot(model_history.history['val_loss'], color='coral')
plt.title("Model Loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["train loss", "test loss"], loc='upper right')
plt.show()