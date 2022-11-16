from flask import Flask
from flask import flash, request, redirect, render_template, url_for
from cloudant.client import Cloudant
from cvlib.object_detection import draw_bbox

import time
import os
import cvlib as cv
import cv2
import time
import numpy as np

app = Flask(__name__)
client = Cloudant.iam(
    'c56fd99d-acbb-4081-8351-ed1e1e82ba02-bluemix', 
    'RKYFESfjUudW-C8Pm-2WaAn3Q9N4Ud49q2PzIbVV4NdU', 
    connect=True)
db = client['user_details']

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def home():
    return render_template('index.html', title="VirtualEye - Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        x = [x for x in request.form.values()]
        data = {
        '_id' : x[0],
        'psw': x[1]
        }
        query = {'_id': {'$eq' : data['_id']}}
        docs = db.get_query_result(query)
        if len(docs.all()) == 0:
            db.create_document(data)
            return render_template('login.html', title='VirtualEye - Login', status='NR')
        else:
            if x[0] == docs[0][0]['_id'] and x[1] == docs[0][0]['psw']:
                return redirect(url_for('prediction'))
            else:
                return render_template('login.html', title="VirtualEye - Login", status="Failed")
    return render_template('login.html', title="VirtualEye - Login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        x = [x for x in request.form.values()]
        data = {
        '_id' : x[1],
        'name': x[0],
        'psw': x[2]
        }
        query = {'_id': {'$eq' : data['_id']}}
        docs = db.get_query_result(query)
        if len(docs.all()) == 0:
            db.create_document(data)
            return render_template('register.html', title='VirtualEye - Register', status='Success')
        else:
            return render_template('register.html', title='VirtualEye - Register', status='Failed')
    return render_template('register.html', title='VirtualEye - Register')

@app.route("/demo", methods=['GET'])
def demo():
    return render_template('base.html', title="VirtualEye - Demo")

@app.route("/forgotpassword")
def forgotpass():
    return render_template('base.html', title="VirtualEye")

@app.route("/logout")
def logout():
    return render_template('logout.html', title="VirtualEye - Logged out")

@app.route('/result')
def prediction():
    webcam = cv2.VideoCapture('drowning.mp4')

    if not webcam.isOpened():
        flash("Could not open webcam")
        exit()
    
    t0 = time.time()
    centre0 = np.zeros(2)
    isDrowning = False

    while webcam.isOpened():
        status, frame = webcam.read()

        bbox, label, conf = cv.detect_common_objects(frame)

        if len(bbox) > 0:
            centre = [0, 0]
            centre = [(bbox[0][0] + bbox[0][2]) / 2, (bbox[0][1] + bbox[0][3]) / 2]
            hmov = abs(centre[0] - centre0[0])
            vmov = abs(centre[1] - centre0[1])

            x = time.time()
            threshold = 10

            if hmov > threshold or vmov > threshold:
                print(x - t0, 's')
                t0 = time.time()
                isDrowning = False
            else:
                print(x - t0, 's')
                if time.time() - t0 > 10:
                    isDrowning = True

            print('bbox:', bbox, ' center:', centre, ' centre0:', centre0)
            print('Are they drowning: ', isDrowning)

            centre0 = centre
        
        out = draw_bbox(frame, bbox, label, conf)

        cv2.imshow("Real-time object detection", out)

        if isDrowning:
            os.system("mpg123 -q alarm.mp3")
            webcam.release()
            cv2.destroyAllWindows()
            return render_template('prediction.html', prediction="Emergency!!! The Person is drowning", title="VirtualEye - Prediction")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
    return render_template('prediction.html', title='VirtualEye - Prediction', prediction='Waiting for footage')


if __name__ == '__main__':
    app.run(debug=True)