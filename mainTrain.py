import cv2
import os
from PIL import Image
from cv2 import norm
from sklearn import metrics
import tensorflow as tf

import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import normalize
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense

image_directory = 'Dataset/'
no_tumor_images = os.listdir(image_directory + 'non_tumorous/')
yes_tumor_images = os.listdir(image_directory + 'tumorous/')
dataset = []
label = []
INPUT_SIZE = 64
#print(no_tumor_images)

for i , image_name  in enumerate(no_tumor_images):
    if(image_name.split('.')[1]=='jpg'):
        image = cv2.imread(image_directory+'non_tumorous/'+image_name)
        image = Image.fromarray(image,'RGB')
        image = image.resize((INPUT_SIZE,INPUT_SIZE))
        dataset.append(np.array(image))
        label.append(0)

for i , image_name  in enumerate(yes_tumor_images):
    if(image_name.split('.')[1]=='jpg'):
        image = cv2.imread(image_directory+'tumorous/'+image_name)
        image = Image.fromarray(image,'RGB')
        image = image.resize((INPUT_SIZE,INPUT_SIZE))
        dataset.append(np.array(image))
        label.append(1)
        
dataset = np.array(dataset)
label = np.array(label)

x_train, x_test, y_train, y_test = train_test_split(dataset,label,test_size=0.2, random_state=0)

print(x_train.shape)

x_train = normalize(x_train, axis=1)
x_test = normalize(x_test,axis=1)

#Model
model = Sequential()

model.add(Conv2D(32,(3,3),input_shape = (INPUT_SIZE,INPUT_SIZE,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3),kernel_initializer='he_uniform'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3),kernel_initializer='he_uniform'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

#Binary CrossEntropy = 1
#Cross Entropy = 2

model.compile(loss = 'binary_crossentropy', optimizer='adam',metrics=['accuracy'])

model.fit(x_train,y_train, 
            batch_size=16,verbose=1, 
            epochs=10, 
            validation_data=(x_test,y_test), 
            shuffle=False
        )
model.save('BrainTumor10Epochs.h5')



