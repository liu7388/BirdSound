# 引入函式庫
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.utils import to_categorical

# 建立卷積神經網路
"""
卷積層(基底32/卷積核3*3/激活relu)
池化層(池化窗口大小2*2)
卷積層(基底64/卷積核3*3/激活relu)
池化層(池化窗口大小2*2)
扁平層
全連接層(輸出1024/激活relu)
全連接層(輸出4/激活softmax)
"""
model = Sequential(name="Model")

# block 1
model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=(45, 21, 1), activation='relu', padding='same',
                 name='block_1_conv'))  # 接收圖片為45*21且為灰階(1)
model.add(MaxPooling2D(pool_size=(2, 2), name='block_1_pool'))
# block 2
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same', name='block_2_conv'))
model.add(MaxPooling2D(pool_size=(2, 2), name='block_2_pool'))
# 扁平層
model.add(Flatten(name="flatten"))
# 全連階層
model.add(Dense(1024, activation='relu', name="Dense_1"))
model.add(Dense(4, activation='softmax', name="Dense_2"))  # 分四種鳥類

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

"""
#載入資料
(train_images,train_labels),(test_images,test_labels)=birdsound.load_data()
//birdsound 為資料處理完後的封裝
**封裝後要存入的矩陣形狀：
train_images=(50000,45,21,1)
train_labels=(50000,1)
test_images=(10000,45,21,1)
test_labels=(10000,1)
# 資料前處理
train_images=train_images.astype('float32')/255  #把輸入的灰度值/255，使其在0與1間
test_images=test_images.astype('float32')/255
train_labels=to_categorical(train_labels)     #One Hot Encoding
test_labels=to_categorical(test_labels)
# 訓練階段
訓練資料/訓練標籤/疊代10次/每次訓練抓200個樣本
model.fit(train_images,train_labels,epochs=10,batch_size=200)
# 測試階段
train_loss,train_acc=model.evaluate(train_images,train_labels)
test_loss,test_acc=model.evaluate(test_images,test_labels)
print("\nTrain loss:", train_loss, "Train Accuracy:", train_acc)
print("Test loss", test_loss, "Test Accuracy:", test_acc)
"""