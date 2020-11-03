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

class VideoCamera(object):
	def __init__(self):
		# Video Capture
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		# Releases camera
		self.video.release()

	def get_frame(self):
		# Extract frames for camera
		ret, frame = self.video.read()
		ret, jpeg = cv2.imencode('.jpg', frame)

		return jpeg.tobytes()

