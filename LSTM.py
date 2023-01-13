# 引入函式庫
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Flatten
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

#建立LSTM模型
"""
LSTM
Dropout層(比率為0.2)
LSTM
Dropout層(比率為0.2)
LSTM
扁平層
全連接層(輸出1024/激活relu)
全連接層(輸出4/激活softmax)
"""
model2 = Sequential(name="Model2")

# block 1
model2.add(LSTM(units=50, return_sequences=True, input_shape=(21, 45)))
# return_sequences為True，輸出三維 (batch_size, time_step, units)
model2.add(Dropout(0.2))
# block 2
model2.add(LSTM(units=50, return_sequences=True))
model2.add(Dropout(0.2))
# block 3
model2.add(LSTM(units=50, return_sequences=True))
# 扁平層
model2.add(Flatten(name="flatten"))
# 全連階層
model2.add(Dense(1024, activation='relu', name="Dense_1"))
model2.add(Dense(4, activation='softmax', name="Dense_2"))  # 分四種鳥類

model2.compile(optimizer='Adam', loss='mean_squared_error', metrics=['accuracy'])
print(model2.summary())

# 建立提早結束CALLBACK2
# validation accuracy 四個執行週期沒改善就停止訓練
callback2 = [tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=4, verbose=1, mode='max')]

# 載入資料
train_images = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\train-images-idx3.npy', allow_pickle=True)
train_labels = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\train-labels-idx1.npy', allow_pickle=True)
test_images = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\t10k-images-idx3.npy', allow_pickle=True)
test_labels = np.load(r'C:\Users\jocy3\Desktop\教學\深度學習\專案\BirdSound\data\label\t10k-labels-idx1.npy', allow_pickle=True)

# 資料前處理
train_images=train_images.astype('float32')/255  #把輸入的灰度值/255，使其在0與1間
test_images=test_images.astype('float32')/255
train_labels=to_categorical(train_labels)     #One Hot Encoding
test_labels=to_categorical(test_labels)
train_images = train_images.reshape(-1, 21, 45, 1)
test_images = test_images.reshape(-1, 21, 45, 1)

# 訓練階段
# 訓練資料/訓練標籤/疊代40次/每次訓練抓80個樣本
model2_history = model2.fit(train_images, train_labels, epochs=40, batch_size=80, callbacks=callback2, validation_data=(test_images, test_labels))

# 測試階段
train_loss,train_acc = model2.evaluate(train_images,train_labels)
test_loss,test_acc = model2.evaluate(test_images,test_labels)
print("\nTrain loss:", train_loss, "Train Accuracy:", train_acc)
print("Test loss", test_loss, "Test Accuracy:", test_acc)

#存成HDF5檔
model2.save('model2.h5')

# 輸出預測圖
# ACCURACY
plt.figure()
plt.plot(model2_history.history['accuracy'], color='darkcyan')
plt.plot(model2_history.history['val_accuracy'], color='coral')
plt.title("Model Accuracy")
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(["train accuracy", 'test accuracy'], loc='lower right')
plt.show()
# LOSS
plt.figure()
plt.plot(model2_history.history['loss'], color='darkcyan')
plt.plot(model2_history.history['val_loss'], color='coral')
plt.title("Model Loss")
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.legend(["train loss", "test loss"], loc='upper right')
plt.show()