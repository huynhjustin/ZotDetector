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
import cv2

# Get user supplied values from .xml file
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

class VideoCamera(object):
	def __init__(self):
		# Video Capture
		self.video = cv2.VideoCapture(0)
	# EOF #

	def __del__(self):
		# Releases camera
		self.video.release()
	# EOF #

	def get_frame(self):
		# Extract frames for camera
		ret, frame = self.video.read()

		# Gray scale frame for face detection
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100),)

		# Iterate to find faces and draw rectangles around them
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		# Converts frame to .jpg for flask	
		ret, jpeg = cv2.imencode('.jpg', frame)

		return jpeg.tobytes()
	# EOF #

