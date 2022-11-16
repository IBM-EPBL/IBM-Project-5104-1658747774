import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import numpy as np
import easygui
from keras.models import load_model
import os
import serial
import time
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
      prediction2 = 'Human Drowning Detected'
      SerialObj = serial.Serial('COM7')
      SerialObj.baudrate = 9600
      SerialObj.bytesize = 8
      SerialObj.parity   ='N'
      SerialObj.stopbits = 1
      time.sleep(3)
      SerialObj.write(b'a')
      SerialObj.close()  

      #ser = serial.Serial("COM7", 9600)
      #data = "X61"  # a  -> Human
      #ser.write(data)
      #s = ser.read(9)
   else:
      prediction2 = 'AnimalDrowning Detected'
      SerialObj = serial.Serial('COM7')
      SerialObj.baudrate = 9600
      SerialObj.bytesize = 8
      SerialObj.parity   ='N'
      SerialObj.stopbits = 1
      time.sleep(3)
      SerialObj.write(b'a')
      SerialObj.close()

##      ser = serial.Serial("COM7", 9600)
##      data = "X62"  # b -> Animal
##      ser.write(data)
##      s = ser.read(9)


else:
   prediction2 = 'Normal '
   SerialObj = serial.Serial('COM6')
   SerialObj.baudrate = 9600
   SerialObj.bytesize = 8
   SerialObj.parity   ='N'
   SerialObj.stopbits = 1
   time.sleep(3)
   SerialObj.write(b'a')
   SerialObj.close()

##   ser = serial.Serial("COM7", 9600)
##   data = "X63"  # c -> Empty
##   ser.write(data)
##   s = ser.read(9)


print(prediction2)
