import sys, os
from binary_classifier_CNN import bcCNN


def get_classifiers(directory="./classifiers"):
    """
    input: the directory the classifiers are being stored
    output: a list of all the classifiers
    allows us to create one set of classifiers that we can reuse
    it helps to avoid a problem where tensorflow does not let you redeclare classifiers
    """

    classifiers = {}
    for path in list(os.walk("classifiers"))[1:]:
        model_path = path[0]
        net = bcCNN.Net(model_path)
        category = model_path.split('/')[1]
        classifications[category] = net

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
