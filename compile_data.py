import numpy as np
import PIL
from PIL import Image

def compile_data():
	images = []
	labels = []
	test_images = []
	test_labels = []

	for i in range(10):
		try:
			tmp_label = np.load('shirts_dataset/labels/out'+str(i)+'.npy')
			print 'a'
		except:
			continue
		try:
			tmp_pic = Image.open('shirts_dataset/images/out'+str(i))
			tmp_pic = tmp_pic.resize((128,128), PIL.Image.ANTIALIAS)
			tmp_pic.show()
			print 'b'
		except:
			continue
		tmp_label = tmp_label.reshape(5)
		pic_array = np.array(tmp_pic)
		if i == 0:
			first_label = tmp_label.tolist()
			first_pic = np.asfarray(pic_array, dtype='float32')/255
			first_pic = np.asarray(first_pic).reshape(-1)
		else:
			labels.append(tmp_label.tolist())
			next_pic = np.asfarray(pic_array, dtype='float32')/255
			next_pic = np.asarray(next_pic).reshape(-1)
			if i == 1:
				images = np.concatenate(([first_pic],[next_pic]),axis=0)
			else:
				images = np.concatenate((images,[next_pic]), axis=0)
	try:
		labels = np.append([first_label],labels, axis=0)
		labels = np.asfarray(labels, dtype='float32')

		np.save('train_labels.npy', labels)
		np.save('train_images.npy', images)
		np.save('test_labels.npy', labels)
		np.save('test_images', images)
	except:
		print "something went wrong"

	return "done"

print compile_data()