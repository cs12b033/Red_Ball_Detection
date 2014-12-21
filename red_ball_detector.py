import cv2 
import numpy as np 
import time
import my_lib

cap = cv2.VideoCapture(0) 
# time.sleep(3)
terminate = 'FALSE'
# while(1): 
# for i in range(1000):
while(terminate == 'FALSE'):
	# Take each frame 
	_, frame = cap.read() 
	# Convert BGR to HSV 
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
	# define range of blue color in HSV 
	lower_blue = np.array([-10,100,100]) 		##Actually this filter is for red, not blue
	upper_blue = np.array([10,255,255]) 
	# lower_blue = np.array([100,20,20]) 
	# upper_blue = np.array([255,80,80]) 
	# Threshold the HSV image to get only blue colors 
	mask = cv2.inRange(hsv, lower_blue, upper_blue) 
	# mask = cv2.inRange(hsv, upper_blue, lower_blue) 
	# Bitwise-AND mask and original image 
	res = cv2.bitwise_and(frame,frame, mask= mask) 
	# cv2.imshow('frame',frame) 
	# cv2.imshow('mask',mask) 
	gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	ball, ball_color = my_lib.detect_circle(gray, frame)
	marked_image = frame
	if(ball != None):
		marked_image = my_lib.mark_image(frame, ball)
	cv2.imwrite("res.jpg", res)
	cv2.imshow('res',res) 
	cv2.imshow('Marked', marked_image)
	k = cv2.waitKey(5) & 0xFF 
	if k == 27: 
		break 
cv2.destroyAllWindows()