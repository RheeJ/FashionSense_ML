import tensorflow as tf
import sys
from binary_classifier_CNN import bcCNN

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "usage:"
        print "python bcCNN.py <old/model/path>"
        exit()

    args = sys.argv[1:]

    old_path = args[0]

    X = tf.placeholder(tf.float32, shape=[None, 64, 64, 3], name='X')
    p_hidden = tf.placeholder(tf.float32, name='p_hidden')
    model = bcCNN.model(X, '', p_hidden)

    sess = tf.Session()
    saver = tf.train.Saver()

    model_location = old_path + 'model.ckpt'
    print model_location
    exit()
    model_meta_path = model_location + '.meta'

    saver = tf.train.import_meta_graph(model_meta_path)
    saver.restore(sess, tf.train.latest_checkpoint(model_path))

    saver.save(sess, old_path + "_new")
