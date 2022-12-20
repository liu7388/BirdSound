import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, LSTM
from keras.utils import to_categorical

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
# 建立提早結束CALLBACK
callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=4, verbose=1, mode='max')]

model2 = Sequential()
model2.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model2.add(Dense(1, activation='sigmoid'))
model2.compile(optimizer='adam', loss="binary_crossentropy", metrics=['accuracy'])

history=model2.fit_generator(generator=train_images.generator(batch_size=200, mode="train"),
                            steps_per_epoch=int(np.ceil(len(train_images.df_train)/200)),
                                                epochs=10,
                                                verbose=1,
                                                callbacks=callbacks,
                                                validation_data=train_images.generator(batch_size=200, mode='val'),
                                                validation_steps=int(np.ceil(len(train_images.df_val)/200)))