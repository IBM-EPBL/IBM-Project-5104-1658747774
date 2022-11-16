import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np
import easygui
import os
import serial

print(tf.__version__)

#feature training
train_datagen = ImageDataGenerator(

        # reducing/normalizing the pixels
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
#connecting the image augmentation tool to our dataset
train_set = train_datagen.flow_from_directory(
        'Class2/training_set',
        #final size of the images that will be fed into the ann
        target_size=(64, 64),
        # number of images that we want to have in each batch
        batch_size=32,
        # we have binary classification --> binary class mode
        class_mode='binary')


#only rescaling but no transformations
test_datagen = ImageDataGenerator(rescale=1./255)
#connecting to the test data
test_set = test_datagen.flow_from_directory(
        'Class2/test_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

print(test_set)

#--------------------- Building CNN --------------------#
# initializing CNN as sequential layers
cnn = tf.keras.models.Sequential()

# Step 1: Convolution to get the Feature Map
cnn.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu', input_shape=[64,64,3]))

# Step 2: Max Pooling
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))
#adding a second convolutional layer
cnn.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))

# Step 3: Flattening
cnn.add(tf.keras.layers.Flatten())

# Step 4: Full Connection
cnn.add(tf.keras.layers.Dense(units = 128, activation = 'relu'))

# Step 5: Output Layer
cnn.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

#--------------------- Training the CNN --------------------#
#compiling the CNN
cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#training the CNN on the training set and evaluating it on the test set
cnn.fit(x = train_set, validation_data = test_set, epochs = 25)
cnn.save('model/save1',overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None,
    save_traces=True,)
cnn.save('model/Class2/model_Class2.h5')


# Testing
image11 = easygui.fileopenbox()
test_image2 = image.load_img(image11, target_size = (64, 64))
test_image2 = image.img_to_array(test_image2)
test_image2 = np.expand_dims(test_image2, axis = 0)
# cnn prediction on the test image
result2 = cnn.predict(test_image2)
print(result2)
if result2[0][0] == 1:
   prediction2 = 'Human'
else:
   prediction2 = 'Animal'


print(prediction2)