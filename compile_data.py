import numpy as np
import PIL
from PIL import Image
from mat_to_npy import deserialize

def compile_data():
	images = []
	labels = []
	test_images = []
	test_labels = []
	first = True
	second = False
	for i in range(1,500):
		try:
			tmp_pic = Image.open('training_pictures/train'+str(i)+'.jpg')
			tmp_pic = tmp_pic.resize((128,128), PIL.Image.ANTIALIAS)
			tmp_pic.save('visualize/train/out'+str(i)+'.jpg')
			pic_array = np.array(tmp_pic)
		except:
			print "exception"
			continue
		if first == True:
			first_pic = np.asfarray(pic_array, dtype='float32')/255
			first_pic = np.asarray(first_pic).reshape(-1)
			labels = deserialize('clothing-data/labels/black_GT.mat', i, labels)
			first = False
			second = True
		else:
			next_pic = np.asfarray(pic_array, dtype='float32')/255
			next_pic = np.asarray(next_pic).reshape(-1)
			labels = deserialize('clothing-data/labels/black_GT.mat', i, labels)
			if second == True:
				images = np.concatenate(([first_pic],[next_pic]),axis=0)
				second = False
			else:
				images = np.concatenate((images,[next_pic]), axis=0)
	try:
		a = np.array(labels)
		print a
		#np.save('train_labels.npy', a)
		#np.save('train_images.npy', images)
	except:
		print "something went wrong"
	first = True
	second = False
	for i in range(501,550):
		try:
			tmp_pic = Image.open('training_pictures/train'+str(i)+'.jpg')
			tmp_pic = tmp_pic.resize((128,128), PIL.Image.ANTIALIAS)
			tmp_pic.save('visualize/test/out'+str(i)+'.jpg')
			pic_array = np.array(tmp_pic)
		except:
			print "exception"
			continue
		if first == True:
			first_pic = np.asfarray(pic_array, dtype='float32')/255
			first_pic = np.asarray(first_pic).reshape(-1)
			test_labels = deserialize('clothing-data/labels/black_GT.mat', i, test_labels)
			first = False
			second = True
		else:
			next_pic = np.asfarray(pic_array, dtype='float32')/255
			next_pic = np.asarray(next_pic).reshape(-1)
			test_labels = deserialize('clothing-data/labels/black_GT.mat', i, test_labels)
			if second == True:
				test_images = np.concatenate(([first_pic],[next_pic]),axis=0)
				second = False
			else:
				test_images = np.concatenate((test_images,[next_pic]), axis=0)
	try:
		a = np.array(test_labels)
		print a
		#np.save('test_labels.npy', a)
		#np.save('test_images.npy', test_images)
	except:
		print "something went wrong"
	return "done"

print compile_data()