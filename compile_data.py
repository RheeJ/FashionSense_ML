import numpy as np
import PIL
from PIL import Image

def compile_data():
	images = []
	labels = []
	test_images = []
	test_labels = []

	for i in range(1,1701):
#		try:
#			tmp_label = np.load('shirts_dataset/labels/out'+str(i)+'.npy')
#		except:
#			continue
#		try:
		tmp_pic = Image.open('clothing-data/images/{:06d}.jpg'.format(i))
		tmp_pic = tmp_pic.resize((128,128), PIL.Image.ANTIALIAS)
#		except:
#			continue
#		tmp_label = tmp_label.reshape(5)
		pic_array = np.array(tmp_pic)
#		if pic_array.shape != (128, 128, 3):
#			continue
		if i == 1:
#			first_label = tmp_label.tolist()
			first_pic = np.asfarray(pic_array, dtype='float32')/255
			first_pic = np.asarray(first_pic).reshape(-1)
		else:
#			labels.append(tmp_label.tolist())
			next_pic = np.asfarray(pic_array, dtype='float32')/255
			next_pic = np.asarray(next_pic).reshape(-1)
			if i == 2:
				images = np.concatenate(([first_pic],[next_pic]),axis=0)
			else:
				images = np.concatenate((images,[next_pic]), axis=0)
	try:
#		labels = np.append([first_label],labels, axis=0)
#		labels = np.asfarray(labels, dtype='float32')

#		print labels.shape
#		print images.shape
#		np.save('train_labels.npy', labels)
		np.save('train_images.npy', images)
	except:
		print "something went wrong"

	for i in range(1701, 1801):
#		try:
#			tmp_label = np.load('shirts_test/labels/out'+str(i)+'.npy')
#		except:
#			continue
		try:
			tmp_pic = Image.open('clothing-data/images/{:06d}.jpg'.format(i))
			tmp_pic = tmp_pic.resize((128,128), PIL.Image.ANTIALIAS)
		except:
			continue
#		tmp_label = tmp_label.reshape(5)
		pic_array = np.array(tmp_pic)
#		if pic_array.shape != (128, 128, 3):
#			continue
		if i == 1701:
#			first_label = tmp_label.tolist()
			first_pic = np.asfarray(pic_array, dtype='float32')/255
			first_pic = np.asarray(first_pic).reshape(-1)
		else:
#			test_labels.append(tmp_label.tolist())
			next_pic = np.asfarray(pic_array, dtype='float32')/255
			next_pic = np.asarray(next_pic).reshape(-1)
			if i == 1702:
				test_images = np.concatenate(([first_pic],[next_pic]),axis=0)
			else:
				test_images = np.concatenate((test_images,[next_pic]), axis=0)
	try:
#		test_labels = np.append([first_label],test_labels, axis=0)
		test_labels = np.asfarray(test_labels, dtype='float32')

#		print test_labels.shape
#		print test_images.shape
#		np.save('test_labels.npy', test_labels)
		np.save('test_images.npy', test_images)
	except:
		print "something went wrong"
	return "done"

print compile_data()