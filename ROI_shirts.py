import cv2
import numpy as np
def extract_shirt(image, counter):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cascade = cv2.CascadeClassifier('haarcascade_mcs_upperbody.xml')
	rects = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(20,20))
	ROI_list = []
	for (i, (x,y,w,h)) in enumerate(rects):
		some_val = h/2
		ROI_list.append(image[y+h-some_val:y+(2*h),x:x+w])
	for i,pic in enumerate(ROI_list):
		if i == 0:
			cv2.imwrite('training_pictures/train'+str(counter)+'.jpg', pic)
	return 'done'
def loadimages():
	for i in range(1,1500):
		image = cv2.imread('clothing-data/images/{:06d}.jpg'.format(i))
		extract_shirt(image, i)
		print 'finished saving {:05}'.format(i)
	return 'done'
print loadimages()

