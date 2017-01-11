import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.layers import flatten
from logger_config import log

np.set_printoptions(threshold='nan')

def loaddata():
	"""
	Function to format our data and compile into tensorflow feed format.

	Input: something
	Output: np_array([[...][...][...]])
	where each [...] is a flattened array

	We could also attempt formatting as CIFAR-10 data with RGB values.
	"""
	images = np.load('train_images.npy')
	labels = np.load('train_labels.npy')

	test_images = np.load('test_images.npy')
	test_labels = np.load('test_labels.npy')

	print "DONE LOADING"
	return (images, labels, test_images, test_labels)

def model(data_x):

	#Declare weight and bias matrices for net.
	#Each convolution weight matrix has kernel size 5x5 with ? depth and ? filters
	c1_w = tf.Variable(tf.truncated_normal([5,5,3,32], stddev=.01))
	c2_w = tf.Variable(tf.truncated_normal([5,5,32,64], stddev=.01))
	c3_w = tf.Variable(tf.truncated_normal([5,5,64,128], stddev=.01))

	#Fully connected layer weights must match output matrix after pooling after the 3rd convolutional layer.
	#So the size of this weights matrix will depend on the image size.
	#For example, we will use 128x128 grayscale image with 10 possible outputs. 3 pooling layers and padding="SAME" so 128/2/2/2 = 16
	fc4_w = tf.Variable(tf.truncated_normal([128 * 16 * 16, 2048], stddev=.01))
	fc5_w = tf.Variable(tf.truncated_normal([2048, 5], stddev=.01))

	#Biases must match shape of weights
	c1_b = tf.Variable(tf.constant(.1, shape=[32]))
	c2_b = tf.Variable(tf.constant(.1, shape=[64]))
	c3_b = tf.Variable(tf.constant(.1, shape=[128]))
	fc4_b = tf.Variable(tf.constant(.1, shape=[2048]))
	fc5_b = tf.Variable(tf.constant(.1, shape=[5]))

	c1 = tf.nn.conv2d(data_x, c1_w, strides=[1,1,1,1], padding='SAME') + c1_b
	c1 = tf.nn.relu(c1)
	c1 = tf.nn.max_pool(c1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

	#print conv_l1.shape()

	c2 = tf.nn.conv2d(c1, c2_w, strides=[1,1,1,1], padding='SAME') + c2_b
	c2 = tf.nn.relu(c2)
	c2 = tf.nn.max_pool(c2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

	c3 = tf.nn.conv2d(c2, c3_w, strides=[1,1,1,1], padding='SAME') + c3_b
	c3 = tf.nn.relu(c3)
	c3 = tf.nn.max_pool(c3, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

	fc4 = tf.reshape(c3, [-1, 128 * 16 * 16])
	fc4 = tf.matmul(fc4, fc4_w) + fc4_b
	fc4 = tf.nn.relu(fc4)

	fc5 = tf.matmul(fc4, fc5_w) + fc5_b

	return fc5

def train(learn_rate):
	train_x, train_y, test_x, test_y = loaddata()
	train_x = train_x.reshape(-1, 128, 128, 3)
	test_x = test_x.reshape(-1, 128, 128, 3)
	X = tf.placeholder(tf.float32, [None, 128, 128, 3])
	Y = tf.placeholder(tf.float32, [None, 5])
	logits = model(train_x)
	cost = tf.nn.softmax_cross_entropy_with_logits(logits, Y)
	train_step = tf.train.AdamOptimizer(learn_rate).minimize(cost)
	with tf.Session() as sess:
		tf.initialize_all_variables().run()
		#determining iterations
		for i in range(100):
			#determining batch size
			for start, end in zip(range(0, len(train_x), 128), range(128, len(train_x)+1, 128)):
				sess.run(train_step, feed_dict={X: train_x[start:end], Y: train_y[start:end]})
			print sess.run([tf.argmax(test_y, 1), tf.argmax(logits,1)], feed_dict={X: test_x, Y: test_y})

log('c_nn')
print train(.001)