import cv2
import sys
import copy
import numpy
import os
import cv
import os.path

#imagePath = "hand.jpeg"
imagePath = sys.argv[1]
# Read the haar cascade classifier file
faceCascade = cv2.CascadeClassifier('haarcascade_hand.xml')
haarFace = cv.Load('haarcascade_frontalface_default.xml')
haarEyes = cv.Load('haarcascade_eye.xml')
car_cascade = cv.Load('cars3.xml')

#cars = car_cascade.detectMultiScale(imagePath, 1.008, 5)
#print str(len(cars)) 
# Read the image
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
	path = 'carimg'
	num_files = len([f for f in os.listdir(path)
		if os.path.isfile(os.path.join(path, f))])
	print str(num_files) + "no. of cars"
	cv2.imwrite("carimg/car[" + str(num_files) + "].jpeg", clone_img)
	#os.remove(imagePath)
	#for (x, y, w, h) in faces:
	#	cv2.rectangle(image, (x, y), (x+w, y+h), (10, 255, 10), 4)
	#cv2.imshow("Hands found", image)

if len(faces) > 0:
	original_img = cv2.imread(imagePath)
	clone_img = copy.copy(original_img)
	path = 'handimg'
	num_files = len([f for f in os.listdir(path)
		if os.path.isfile(os.path.join(path, f))])
	print num_files
	cv2.imwrite("handimg/hand[" + str(num_files) + "].jpeg", clone_img)
	#os.remove(imagePath)
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (10, 255, 10), 4)
	cv2.imshow("Hands found", image)

if detectedFace:
	original_img = cv2.imread(imagePath)
	clone_img = copy.copy(original_img)
	path = 'faceimg'
	num_files = len([f for f in os.listdir(path)
		if os.path.isfile(os.path.join(path, f))])
	print num_files
	cv2.imwrite("faceimg/face[" + str(num_files) + "].jpeg", clone_img)
	#os.remove(imagePath)
	for face in detectedFace:
		cv.Rectangle(imcolor,(face[0][0],face[0][1]),
			(face[0][0]+face[0][2],face[0][1]+face[0][3]),
			cv.RGB(155, 255, 25),2)
	cv.NamedWindow('Face Detection', cv.CV_WINDOW_AUTOSIZE)
	cv.ShowImage('Face Detection', imcolor) 

if detectedEyes:
	original_img = cv2.imread(imagePath)
	clone_img = copy.copy(original_img)
	path = 'eyeimg'
	num_files = len([f for f in os.listdir(path)
		if os.path.isfile(os.path.join(path, f))])
	print num_files
	cv2.imwrite("eyeimg/eyes[" + str(num_files) + "].jpeg", clone_img)
	#os.remove(imagePath)
	for face in detectedEyes:
		cv.Rectangle(imcolor,(face[0][0],face[0][1]),
			(face[0][0]+face[0][2],face[0][1]+face[0][3]),
			cv.RGB(155, 55, 200),2)
	cv.NamedWindow('Eyes Detection', cv.CV_WINDOW_AUTOSIZE)
	cv.ShowImage('Eyes Detection', imcolor) 

cv2.waitKey(0)
cv.WaitKey()
