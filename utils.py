import sys, os
from binary_classifier_CNN import bcCNN


def get_classifications(image_path, directory="./classifiers"):

    classifications = {}
    for path in list(os.walk("classifiers"))[1:]:
        model_path = path[0]
        net = bcCNN.Net(model_path)
        print image_path
        classifications[model_path.split('/')[1]] = net.classify(image_path)

    return classifications


if __name__ == "__main__":

    path = sys.argv[1]
    print get_classifications(path)
