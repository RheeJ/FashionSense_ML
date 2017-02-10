import sys, os
from binary_classifier_CNN import bcCNN

log('running')

def _get_classifier_paths(directory):
    paths = []
    for classifier in directory:
        paths.append(directory+"/"+classifier+"/")
    return paths

def _build_classification_dict(directory, paths):
    n = len(directory) + 1
    names = []
    for path in paths:
        names.append(path[n:-1])
    return dict(zip(paths, names))


def _get_classifications(path_dict, image):
    paths = path_dict.keys
    classifications = []
    for path in paths:
        net = bcCNN.Net(path)
        classifications[path_dict[path]] = model_net.classify(filepath)
    return classifications

def do_everything(image, directory="./classifiers"):
    paths = _get_classifier_paths(directory)
    path_dict = _build_classification_dict(directory, paths)
    classifications = _get_classifications(path_dict, image)
    return classifications
