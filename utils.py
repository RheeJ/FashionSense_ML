import sys, os
from binary_classifier_CNN import bcCNN
import base64
import tempfile
from PIL import Image

def decode_base64(data):
    """
    decodes a json object that contains the base64 image data as follows
    { "image":"base64data" }
    """

    image = None
    try:
        image = base64.decodestring(data)
    except:
        print "Could not decode base64 image from json"

    return image

def create_temporary_image(image):
    """
    creates a temporary file object used to store images and returns it
    """

    temp = tempfile.NamedTemporaryFile()
    temp.write(image)
    temp.seek(0)

    return temp

def get_classifiers(directory="/data/classifiers"): #used to be ./classifiers
    """
    input: the directory the classifiers are being stored
    output: a list of all the classifiers
    allows us to create one set of classifiers that we can reuse
    it helps to avoid a problem where tensorflow does not let you redeclare classifiers
    """

    classifiers = {}
    for path in list(os.walk(directory))[1:]:
        model_path = path[0]
        category = model_path.split('/')[2]
        net = bcCNN.Net(directory, category)
        classifiers[category] = net

    return classifiers


def get_classifications(classifiers, image_path):
    """
    input: the classifiers(tensorflow models) we have traind and path of the image to classify
    output: a dictionary containing each classification on the image
    takes the models inside classifiers and walks over them classifying the image
    specified by image path
    """

    classifications = {}
    for key, net in classifiers.iteritems():
        classifications[key] = net.classify(image_path)

    return classifications
