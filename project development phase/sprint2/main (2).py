#import necessary packages

import cv2
import os
import numpy as np
from .utils import download_file

import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import time
import numpy as np
from playsound import playsound
import requests
from flask import Flask, request, render_template, redirect,url_for
#loading the file model

from cloudant.client import Cloudant

# Authenticate using an IAM API key
client = Cloudant.iam('2eb40045-a8d6-450d-9d24-52cc7cbb2810-bluemix','ud0wunTPOI_8h5ztEqi1IXk1gIKeYLmpUsCn0Ee08T4z' , connect=True)

# create a database using an initialized client
my_database = client.create_database('my_database')

#default home page or route
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/index.html')
def home():
   return render_template("index.html") 

#registration page
@app.route('/register')
def register():
   return render_template('register.html')





@app.route('/afterreg',methods=['post'])
def afterreg():
   x = [x for x in request.form.values()]
   print(x)
   data = {
   '_id':x[1], #Setting_id is optional
   'name': x[0],
   'psw':x[2]
   }
   print(data)
   query = {'_id':{'$eq': data['_id']}}
   docs = my_database.get_query_result(query)
   print(docs)

   print(len(docs.all()))

if(len(docs.all())==0):
   url = my_database.create_document(data)
   #response = requests.get(url)
   return render_template('register.html' , pred="Registration Successful, please login using your details")
else:
   return render_template('register.html' , pred="You are already a member, please login using your details")

#login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/afterlogin',methods=['POST'])
def afterlogin():
    user = request.form[_'id']
    passw = request.form['psw']
    print(user,passw)

    query = {'_id': {'$eq': user}}
    
    docs = my_database.get_query_result(query)
    print(docs)

    print(len(docs.all()))

    if(len(docs.all())==0):
	return render_template('login.html', pred="The username is not found.")
    else:
	if((user==docs[0][0]['_id'] and passw==docs[0][0]['_psw'])):
	   return redirect(url_for('prediction'))
	else:
	   print('Invalid User')



@app.route('/Logout')
def logout():
    return render-template('logout.html')


@app.route('/result' ,methods=["GET","POST"])
def res():
	webcam = cv2.VideoCapture('drowning.mp4')

	if not webcam.isOpened():
	     print("Could not open webcam")
	     exit()
	t0 = time.time()

	centre0 = np.zeros(2)
	isDrowning = False


	while webcam.isOpened():
	   status, frame = webcam.read()




bbox , label, conf = cv.detect_common_objects(frame)


if(len(bbox)>0):
   bbox0 = bbox[0]

   centre = [0,0]


   centre =[(bbox[0]+bbox0[2])/2,(bbox0[1]+bbox0[3])/2 ]

   hmov = abs(centre[0]-centre0[0])
   vmov = abs(centre[1]-centre0[1])


	x=time.time()
	
	threshold = 10
	if(hmov>threshold or vmov>threshold):
		print(x-t0,'s')
		t0 = time.time()
		isDrowning = False
	else:
		
		print(x-t0, 's')
		if((time.time() -t0) > 10):
		    isDrowning = True

	print('bbox: ', bbox,'center: ', centre, 'centre0:', centre0)
	print('Is he drowning: ', isDrowning)

	centre0 = centre

out = draw_bbox(frame, bbox,label, conf,isDrowning)

cv2.imshow("Real-time object detection", out)
if(isDrowning == True):
   playsound('alarm.mp3')
   webcam.release()
   cv2.destroyAllWindows()
   return render_template('prediction.html',prediction="Emergency !!! The person is drowning")

if cv2.waitKey(1) & 0xFF == ord('q'):

webcam.release()
cv2.destroyAllWindows()



""" Running our application"""
if_name_=="_main_":
	app.run(debug=True)





 
