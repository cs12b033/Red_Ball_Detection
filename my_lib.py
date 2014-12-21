##
## Objective: Program to detect Red Ball in Any Background
## File: All Functions are written here
## Author: Ajay Pratap Singh
## Date: 20 Dec 2014
##

import cv2
import cv2.cv as cv
import numpy as np
	


def init_camera():
	camera_id = 0
	camera = cv2.VideoCapture(camera_id)
	# camera = cv2.VideoCapture("ball1.avi")
	return camera
	
	
def take_picture(camera):
	retval, img = camera.read()
	return img
	
	
def release_camera(camera): 
	del(camera)

	
def detect_circle(gray, img):
	"""Find circles on the given image"""
	# Reduce the noise to avoid false circle detection
	gray_blured = cv2.medianBlur(gray, 27)
	cv2.imwrite("blur.jpg", gray_blured)
	#Apply the Hough transform to find the circles
	circles = cv2.HoughCircles(gray_blured, cv.CV_HOUGH_GRADIENT,
	1, 20, param1 = 50, param2 = 5, minRadius = 2, maxRadius = 0) #50 30
	
	if(circles == None):
		ball_color = 'UNKNOWN'
		return None, ball_color
	
	#Round to integers 
	circles = np.uint16(np.around(circles)) 			## "uint"  not unit
	
	# found = 1
	for i in circles[0, :]:
		ball_color = detect_color(img, i)
		if(ball_color == 'RED'):
			# found = 0
			print "\tRed ball found!"
			break;
		# else:
			# print "Circle check...", ball_color
	# ball = circles[0][0]
	ball = i
	# print "Ball => ", ball
	return ball, ball_color
	
	
def detect_color(image, ball):
	"""Recognize the color of the detected ball"""
	#Crop the ball region for color detection
	#[y1:y2, x1:x2], x1y1 -top left, x2y2 - bottom right
	ball_img = image[ball[1] - ball[2]/2 : ball[1]+ball[2]/2,
		ball[0] - ball[2]/2 : ball[0] + ball[2]/2]
	cv2.imwrite("crop.jpg", ball_img)
	#Convert cropped image to HSV
	ball_img = cv2.cvtColor(ball_img, cv2.COLOR_BGR2HSV)
	cv2.imwrite("crop1.jpg", ball_img)
	# get Color
	ball_hsv_mean = cv2.mean(ball_img)
	hue = ball_hsv_mean[0]
	
	if(hue < 11):
		color = 'RED'
	elif (hue < 18):
		color = 'ORANGE'
	elif (hue < 39):
		color = 'YELLOW'
	elif (hue < 76):
		color = 'GREEN'
	elif (hue < 131):
		color = 'BLUE'
	elif (hue < 161):
		color = 'VIOLET'
	elif (hue < 180):
		color = 'RED'
	else:
		color = 'UNKNOWN'
	return color
		
		
def mark_image(image, ball):
	"""Mark the detected ball on the image"""
	# Draw the outer circle
	cv2.circle(image, (ball[0], ball[1]), ball[2], (0, 255, 0), 2)
	#Draw the centre of the circle
	cv2.circle(image, (ball[0], ball[1]), 2, (0, 128, 255), 3)
	return image