import tensorflow as tf
import numpy as np

np.set_printoptions(threshold='nan')

class lstm(object):
	def __init__(self):
		self.sess = tf.Session()

		self.X = tf.placeholder(tf.float32, [None, 256, 14*14])
		self.Y = tf.placeholder(tf.float32, [None, 1])
		self.lstm_size = 14*14
		self.W = tf.Variable(tf.truncated_normal([2*self.lstm_size, 1], stddev=0.01))
		self.B = tf.Variable(tf.constant(.1, shape=[1]))

		self.time_step_size = 256

		self.logits = self.model(self.X)
		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.logits, self.Y))
		self.train_step = tf.train.RMSPropOptimizer(.001, .9).minimize(self.cost)
		self.prediction = tf.greater(self.logits, 0)
		self.correct_answer = Y
		self.saver = tf.train.Saver()

	def model(self, X):
		XT = tf.transpose(X, [1,0,2])
		#Time Major: shape of XT (time_step, batch_size, input)
		XR = tf.reshape(XT, [-1, self.lstm_size])
		#Reshape: shape of XT (time_step * batch_size, input)
		XS = tf.split(0, self.time_step_size, XR)
		#Array: Length(256) each array has shape (batch_size, input)
		forward_cell = tf.nn.rnn_cell.BasicLSTMCell(self.lstm_size, forget_bias=1.0, state_is_tuple=True)
		backward_cell = tf.nn.rnn_cell.BasicLSTMCell(self.lstm_size, forget_bias=1.0, state_is_tuple=True)
		outputs, _, _ = tf.nn.bidirectional_rnn(forward_cell, backward_cell, XS, dtype=tf.float32)
		fc_layer = tf.matmul(outputs[-1], self.W) + self.B
		return fc_layer

	def train(self):
		train_X = #function to load train_X
		train_Y = #function to load train_Y
		self.sess.run(tf.global_variables_initializer())
		for i in range(500):
			for start,end in zip(range(0, len(train_X), 128), range(128, len(train_X)+1, 128)):
				try:
					self.sess.run(self.train_op, feed_dict={self.X: train_X[start:end], self.Y: train_Y[start:end]})
				except KeyboardInterrupt:
					print "Saving the Model"
					self.saver.save(self.sess, 'lstm_weights/model.ckpt')
					print "Saved"
					exit()      
		print "Saving the Model"
		self.saver.save(self.sess, 'lstm_weights/model.ckpt')
		print "Saved"

	def classify(self, features_from_conv):
		test_X = #function to load test_X
		ckpt = tf.train.get_checkpoint_state('./lstm_weights/')
		if ckpt and ckpt.model_checkpoint_path:
			self.saver.restore(self.sess, ckpt.model_checkpoint_path)
			return self.sess.run(self.predict_op, feed_dict={self.X: test_X})
		else:
			return "Could not load the model"