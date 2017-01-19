import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import sys
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

"""
Set up TF variables outside of model to save the weights automagically
"""

#Declare weight and bias matrices for net.
#Each convolution weight matrix has kernel size 5x5 with ? depth and ? filters
c1_w = tf.Variable(tf.truncated_normal([5,5,3,32], stddev=.01))
c2_w = tf.Variable(tf.truncated_normal([5,5,32,64], stddev=.01))
c3_w = tf.Variable(tf.truncated_normal([5,5,64,128], stddev=.01))

#Fully connected layer weights must match output matrix after pooling after the 3rd convolutional layer.
#So the size of this weights matrix will depend on the image size.
#For example, we will use 128x128 grayscale image with 10 possible outputs. 3 pooling layers and padding="SAME" so 128/2/2/2 = 16
fc4_w = tf.Variable(tf.truncated_normal([128 * 16 * 16, 2048], stddev=.01))
fc5_w = tf.Variable(tf.truncated_normal([2048, 3], stddev=.01))

#Biases must match shape of weights
c1_b = tf.Variable(tf.constant(.1, shape=[32]))
c2_b = tf.Variable(tf.constant(.1, shape=[64]))
c3_b = tf.Variable(tf.constant(.1, shape=[128]))
fc4_b = tf.Variable(tf.constant(.1, shape=[2048]))
fc5_b = tf.Variable(tf.constant(.1, shape=[3]))

X = tf.placeholder(tf.float32, [None, 128,128, 3])
Y = tf.placeholder(tf.float32, [None, 3])
logits = model(X)
cost = tf.nn.softmax_cross_entropy_with_logits(logits, Y)
train_step = tf.train.AdamOptimizer(.0001).minimize(cost)
predict_step = tf.argmax(logits, axis=1)
correct_prediction =  tf.argmax(Y, axis=1)
saver = tf.train.Saver()
sess = tf.Session()

def train():
	print "Initializing Random Weights"
	sess.run(tf.global_variables_initializer())
	print "Loading Train and Test Data"
	train_x, train_y, test_x, test_y = loaddata()
	train_x = train_x.reshape(-1, 128, 128, 3)
	test_x = test_x.reshape(-1, 128, 128, 3)
	#determining iterations
	print "Start Training"
	for i in range(100):
		try:
			#determining batch size
			for start, end in zip(range(0, len(train_x), 128), range(128, len(train_x)+1, 128)):
				sess.run(train_step, feed_dict={X: train_x[start:end], Y: train_y[start:end]})
			print (i, np.mean(np.argmax(test_y, axis=1) == sess.run(predict_step, feed_dict={X: test_x})))
		except KeyboardInterrupt:
			print "Saving The Model. Please wait:"
			saver.save(sess, 'trained_model.ckpt')
			print "Done Saving Model"
			exit()
	print "Saving The Model. Please wait:"
	saver.save(sess, 'trained_model.ckpt')
	print "Done Saving Model"

def test():
	_,_,test_x,test_y = loaddata()
	test_x.reshape(-1,128,128,3)
	ckpt = tf.train.get_checkpoint_state(".")
	if ckpt and ckpt.model_checkpoint_path:
		print "Loading Trained Weights"
		saver.restore(sess, ckpt.model_checkpoint_path)
		print sess.run((predict_step, correct_prediction), feed_dict={X:test_x, Y:test_y})

if sys.argv[1] == 'train':
	train()
elif sys.argv[1] == 'test':
	test()
else:
	print "You can either train or test. Usage: python c_nn.py train or python c_nn.py test. Validation coming soon."
log('c_nn')
