###By: Jimmy Song
###Decision Tree for Fashion-Style Classification

import sys
import pickle
import sklearn
import numpy as np
import scipy
from logger_config import log
from sklearn import tree

InputFileName = str(sys.argv[1])
Query = str(sys.argv[2])

def preprocess(filename):
    #TODO: Preprocess input file once images have been scraped.
    #Return training set, training labels, testing set, and testing labels as numpy array.
    training_set = np.zeros()
    training_labels = np.zeros()
    testing_set = np.zeros()
    testing_labels = np.zeros()


    return training_set, training_labels, testing_set, testing_labels

def save_classifier(classifier, training_set, training_labels):
    #Saves Classifier for faster runtime in future uses.
    pickle.dump(classifier, open('classifier.p', 'w'))
    pickle.dump(training_set, open('training_set.p', 'w'))
    pickle.dump(training_labels, open('training_labels.p', 'w'))

def main(filename, query):

    log('d_tree')
    training_set, training_labels, testing_set, testing_labels = preprocess(filename)

    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(training_set, training_labels)
    save_classifier(classifier, training_set, training_labels)
    classifier = pickle.load(open('classifier_1.p'))


    #Simple Error Test for Classifier
    #TODO: Cross-Validation Testing for Error Rate
    predicted_labels = classifier.predict(testing_set)
    errorCount = 0
    for i in range(len(testing_set)):
        if testing_labels[i] != predicted_labels[i]:
            errorCount += 1
    errorRate = float(errorCount) / len(testing_set)
    print "Error Rate of Decision_Tree Classifier: " + str(errorRate)

    #Given new Query, Return classification of Query
    result = classifier.predict(query)
    print "Query Classified as: " + str(result)
    return result

main(InputFileName)

