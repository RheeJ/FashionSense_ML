import utils
import tensorflow as tf
import numpy as np
import sys
import os


def conv_layer(X, kernel, strides, number):
    """
    inputs: dimensions of convolutional layers and pooling
    output: the pooling layer
    """
    output_size = kernel[3]

    with tf.name_scope('conv' + str(number)) as scope:
        kernel = tf.Variable(tf.truncated_normal(kernel, dtype=tf.float32,
                                               stddev=1e-1), name='weights')
        conv = tf.nn.conv2d(X, kernel, strides, padding='SAME')
        biases = tf.Variable(tf.constant(0.0, shape=[output_size], dtype=tf.float32),
                           trainable=True, name='biases')
        bias = tf.nn.bias_add(conv, biases)
        conv = tf.nn.relu(bias, name=scope)

    return conv


def pool_layer(X, ksize, kstrides, number):
    """
    inputs: takes in the parameters to create a pooling layer
    output: pooling tensor
    """

    pool = tf.nn.max_pool(X,
                           ksize=ksize,
                           strides=kstrides,
                           padding='SAME',
                           name='pool' + str(number))

    return pool


def full_layer(X, input_size, output_size, number):
    """
    inputs: dimensions of fully connected layer
    output: the fully connected layer
    """

    with tf.name_scope("full" + str(number)) as scope:
        W = tf.Variable(tf.random_normal([input_size, output_size]), name='W')
        b = tf.Variable(tf.constant([output_size], dtype=tf.float32), name='b')
        full = tf.matmul(X, W) + b

    return full


class Net(object):

    @staticmethod
    def compute_accuracy(expected, actual):
        """
        input: the expected and actual
        output: the percent accuracy
        """

        assert(len(expected) == len(actual))

        length_data = len(expected)

        compare = np.array(np.argmax(expected, axis=1) == np.argmax(actual, axis=1))
        correct = (compare == True).sum()

        return (float(correct) / float(length_data)) * 100

    @staticmethod
    def model(X, p_hidden):
        """
        output: return the model
        """

        conv1 = conv_layer(X, [5, 5, 3, 64], [1, 1, 1, 1], 1)
        pool1 = pool_layer(conv1, [1, 2, 2, 1], [1, 2, 2, 1], 1)

        conv2 = conv_layer(pool1, [5, 5, 64, 128], [1, 1, 1, 1], 2)
        pool2 = pool_layer(conv2, [1, 2, 2, 1], [1, 2, 2, 1], 2)

        conv3 = conv_layer(pool2, [3, 3, 128, 256], [1, 1, 1, 1], 3)
        pool3 = pool_layer(conv3, [1, 2, 2, 1], [1, 2, 2, 1], 3)

        reshape_pool3 = tf.reshape(pool3, [-1,  8*8*256])

        full1 = full_layer(reshape_pool3, 8*8*256, 4096, 1)
        full1 = tf.nn.dropout(full1, p_hidden)

        model = full_layer(full1, 4096, 2, 3)

        return model

    def __init__(self, model_path):

        self.sess = tf.Session()
        self.X = tf.placeholder(tf.float32, shape=[None, 64, 64, 3], name='X')
        self.Y = tf.placeholder(tf.float32, shape=[None, 2], name='Y')
        self.p_hidden = tf.placeholder(tf.float32, name='p_hidden')
        self.logits = self.model(self.X, self.p_hidden)
        self.saver = tf.train.Saver()

        self.model_location = model_path + '/' + 'model.ckpt'
        model_meta_path = self.model_location + '.meta'

        self.saved_model = False
        if os.path.isfile(model_meta_path):
            self.saver = tf.train.import_meta_graph(model_meta_path)
            self.saver.restore(self.sess, tf.train.latest_checkpoint(model_path))
            self.saved_model = True

    def train(self, data, labels, validation_data, validation_labels):
        """
        train model
        """

        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
        learning_rate = 0.0001
        optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

        self.sess.run(tf.global_variables_initializer())

        batch_size = 100
        epochs = 100
        print "Accuracy: "

        try:
            for epoch in range(epochs):
                idxs = np.random.permutation(len(data))
                batches = len(data) // batch_size
                for batch in range(batches):
                    idx = idxs[batch * batch_size: (batch + 1) * batch_size]
                    self.sess.run(optimizer, feed_dict={self.X:data[idx], self.Y:labels[idx], self.p_hidden: 0.5})

                # if epoch % 5 == 0:
                output = np.array(self.sess.run(self.logits, feed_dict={self.X: validation_data, self.p_hidden: 1.0}))
                accuracy = self.compute_accuracy(output, validation_labels)
                print "epoch "+ str(epoch) + ": " + str(accuracy) + '%'

        except KeyboardInterrupt:
            print "Saving model before exiting"
            self.saver.save(self.sess, self.model_location)
            self.saved_model = True
            exit()

        print "Saving model"
        self.saver.save(self.sess, self.model_location)

    def test(self, data, labels):
        """
        input: data and labels of test data
        prints out the accuracy on the test data
        """

        if self.saved_model:
            print "Testing..."
            output = self.sess.run(self.logits, feed_dict={self.X:data, self.Y:labels, self.p_hidden: 1.0})
            accuracy = self.compute_accuracy(output, labels)
            print "Accuracy: " + str(accuracy) + '%'
        else:
            print "Model does not exist yet...train first"

    def classify(self, image_path):
        """
        input: path to an image
        output: the classification of that image
        """

        if self.saved_model:
            img = [utils.load_image(image_path)]
            print "classifying..."
            output = np.argmax(self.sess.run(self.logits, feed_dict={self.X: img})[0])
            return output
        else:
            print "Model does not exist yet...train first"

    def __del__(self):
        self.sess.close()


if __name__ == "__main__":

    args = sys.argv[1:]
    def usage_message():
        print "usage:"
        print "python bcCNN.py -train <path/to/images1> <path/to/images2>"
        print "python bcCNN.py -test <path/to/images1> <path/to/images2>"
        print "python bcCNN.py -classify <path/image/to/classify>"
        print "-link <path/to/save/model>"
        exit()

    if len(args) == 2:
        if args[0] == "-classify":
            path = args[1]
            print "classification: " + str(net.classify(path))
            exit()

    if len(args) == 4:
        label_1_images = args[1]
        label_0_images = args[2]
        pathway = args[3]

        #instantiate object Net
        net = Net(pathway)

        if args[0] == "-train":
            data, val_data, labels, val_labels = utils.get_test_and_validation_data(label_1_images, label_0_images)
            print "Initializing training..."
            net.train(data, labels, val_data, val_labels)
            exit()
        if args[0] == "-test":
        	print "here"
        	data, labels = utils.get_data(label_1_images, label_0_images)
        	net.test(data, labels)
        	exit()

    usage_message()
