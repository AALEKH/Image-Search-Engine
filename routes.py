from flask import Flask, render_template
from flask import request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
import cv
import os.path
import cv2
import sys
import copy
import numpy
import redis
  
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def detect():
  arr = os.listdir("uploads")
  imagePath = "uploads/"
  for b in arr:
    imagePath = imagePath + b  
  #r_server = redis.Redis("localhost")
  faceCascade = cv2.CascadeClassifier('haarcascade_hand.xml')
  haarFace = cv.Load('haarcascade_frontalface_default.xml')
  haarEyes = cv.Load('haarcascade_eye.xml')
  car_cascade = cv.Load('cars3.xml')

  imcolor = cv.LoadImage(imagePath) 
  storage = cv.CreateMemStorage()

  detectedFace = cv.HaarDetectObjects(imcolor, haarFace, storage)
  detectedEyes = cv.HaarDetectObjects(imcolor, haarEyes, storage)
  detectedCar  = cv.HaarDetectObjects(imcolor, car_cascade, storage)
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Detect faces in the image
  faces = faceCascade.detectMultiScale(
      gray,
      scaleFactor=1.1,
      minNeighbors=2,
      minSize=(30, 30),
      flags = cv2.cv.CV_HAAR_DO_CANNY_PRUNING
  )

  print len(faces)
  print detectedFace
  print detectedEyes

  if detectedCar > 0:
    original_img = cv2.imread(imagePath)
    clone_img = copy.copy(original_img)
    path = 'cars'
    num_files = len([f for f in os.listdir(path)
      if os.path.isfile(os.path.join(path, f))])
    print str(num_files) + "no. of cars"
    name = "cars/car[" + str(num_files) + "].jpeg"
    cv2.imwrite(name, clone_img)
    #r_server.rpush("Cars", name)

  if len(faces) > 0:
    original_img = cv2.imread(imagePath)
    clone_img = copy.copy(original_img)
    path = 'Hand'
    num_files = len([f for f in os.listdir(path)
      if os.path.isfile(os.path.join(path, f))])
    print num_files
    name = "Hand/hand[" + str(num_files) + "].jpeg"
    cv2.imwrite(name, clone_img)
    #r_server.rpush("Hand", name)

  if detectedFace:
    original_img = cv2.imread(imagePath)
    clone_img = copy.copy(original_img)
    path = 'Face'
    num_files = len([f for f in os.listdir(path)
      if os.path.isfile(os.path.join(path, f))])
    print num_files
    name = "Face/face[" + str(num_files) + "].jpeg"
    cv2.imwrite(name, clone_img)
    #r_server.rpush("Face", name)

  if detectedEyes:
    original_img = cv2.imread(imagePath)
    clone_img = copy.copy(original_img)
    path = 'Eye'
    num_files = len([f for f in os.listdir(path)
      if os.path.isfile(os.path.join(path, f))])
    print num_files
    name = "Eye/eyes[" + str(num_files) + "].jpeg"
    cv2.imwrite(name, clone_img)
    #r_server.rpush("Eye", name)           
  
@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  detect()
  return redirect(url_for('uploaded_file',
                                filename=filename))
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/result', methods=['POST'])
def result():
    search = request.form['search']
    my_list = os.listdir(search)
    elements = [search + "/" + x for x in my_list]
    return render_template('result.html', loopdata = elements)    
  
if __name__ == '__main__':
  app.run(
        host="127.0.0.1",
        port=int("5004"),
        debug=True
    )