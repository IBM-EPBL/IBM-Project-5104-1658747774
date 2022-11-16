import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np
import easygui
from keras.models import load_model
import os
import serial
print(tf.__version__)



model1 = load_model('model/Class1/model_Class1.h5')
model2 = load_model('model/Class2/model_Class2.h5')
# Testing
image11 = easygui.fileopenbox()
test_image2 = image.load_img(image11, target_size = (64, 64))
test_image2 = image.img_to_array(test_image2)
test_image2 = np.expand_dims(test_image2, axis = 0)
# cnn prediction on the test image
result2 = model1.predict(test_image2)
print(result2)
if result2[0][0] == 1:
   result3 = model2.predict(test_image2)
   if result3[0][0] == 1:
      prediction2 = 'Human'
   else:
      prediction2 = 'Animal'


else:
   prediction2 = 'Empty'


print(prediction2)