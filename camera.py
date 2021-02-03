# Import packages
# from imutils.video import VideoStream
# from flask import Response
# from flask import Flask
# from flask import render_template
# import threading
# import argparse
# import datetime
# import imutils
# import time
import numpy as np
import argparse
import cv2
import os
import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# Disable TensorFlow debugging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Get user supplied values from .xml file
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))



class VideoCamera(object):
	def __init__(self):
		# Video Capture
		self.video = cv2.VideoCapture(0)
		self.emotions_count = {"Angry": 0, "Disgusted": 0, "Fearful": 0, "Happy": 0, "Neutral": 0, "Sad": 0, "Surprised": 0}
	# EOF #

	def __del__(self):
		# Releases camera
		self.video.release()
	# EOF #

	def get_frame(self):

		# Load weights from the model .h5 file
		model.load_weights('model.h5')

		emotions_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

		# Extract frames for camera
		ret, frame = self.video.read()

		# Gray scale frame for face detection
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100),)

		# Iterate to find faces and draw rectangles around them
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

			# Get frame in grayscale
			gray_frame = gray[y:y + h, x:x + w]
			cropped_frame = np.expand_dims(np.expand_dims(cv2.resize(gray_frame, (48, 48)), -1), 0)

			# Get prediction and find index for dictionary
			prediction = model.predict(cropped_frame)
			index = int(np.argmax(prediction))

			# Show text of emotion in camera feed
			cv2.putText(frame, emotions_dict[index], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
			print(emotions_dict[index])
			self.emotions_count[emotions_dict[index]] += 1
			#cv2.putText(frame, "[Emotion]", (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

		# Converts frame to .jpg for flask	
		ret, jpeg = cv2.imencode('.jpg', cv2.resize(frame,(300,300),interpolation = cv2.INTER_CUBIC))

		return jpeg.tobytes()
	# EOF #

