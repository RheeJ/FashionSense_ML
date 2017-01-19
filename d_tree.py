###By: Jimmy Song
###Decision Tree for Fashion-Style Classification

import sys
import pickle
import sklearn
import numpy as np
import scipy
import csv
from logger_config import log
from sklearn import tree

InputFileName = str(sys.argv[1])
Query = str(sys.argv[2])

def preprocess(filename):
    #TODO: Preprocess input file once images have been scraped.
    #Return training set, training labels, testing set, and testing labels as numpy array.
    training_set = []
    training_labels = []
    testing_set = []
    testing_labels = []

    #Input File = comma delineated for features, line delineated for each piece of data.
    #Feature Vector consists of 25 features, see README for encoding details.

    with open(filename, 'rb') as csvfile:
        featuresArray = []
        labelsArray = []
        i = 0

        ###Feature we are using correspond to the following indices:
        ###3, 4, 6, 9, 22

        for line in csv.reader(csvfile, dialect="excel"):
            ###i = Number of lines to encode
            if i < 200:
                line = map(int, line)
                featuresArray.append(line[0:26])
                labelsArray.append(line[26])
                i += 1

        training_set = featuresArray[25:200]
        training_labels = labelsArray[25:200]
        testing_set = featuresArray[0:25]
        testing_labels = labelsArray[0:25]

        ##Filter important features, [i][j] where j denotes the feature we use.
        for i in range(len(training_set)):
            temp = []
            temp.append(training_set[i][3])
            temp.append(training_set[i][4])
            temp.append(training_set[i][6])
            temp.append(training_set[i][9])
            temp.append(training_set[i][22])
            training_set[i] = temp
        for i in range(len(testing_set)):
            temp = []
            temp.append(testing_set[i][3])
            temp.append(testing_set[i][4])
            temp.append(testing_set[i][6])
            temp.append(testing_set[i][9])
            temp.append(testing_set[i][22])
            testing_set[i] = temp


    return training_set, training_labels, testing_set, testing_labels

def save_classifier(classifier, training_set, training_labels):
    #Saves Classifier for faster runtime in future uses.
    pickle.dump(classifier, open('classifier.p', 'w'))
    # pickle.dump(training_set, open('training_set.p', 'w'))
    # pickle.dump(training_labels, open('training_labels.p', 'w'))

def main(filename, query):
    log('d_tree')
    training_set, training_labels, testing_set, testing_labels = preprocess(filename)

    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(training_set, training_labels)
    save_classifier(classifier, training_set, training_labels)
    classifier = pickle.load(open('classifier.p'))


    #Simple Error Test for Classifier
    #TODO: Cross-Validation Testing for Error Rate
    predicted_labels = classifier.predict(testing_set)
    errorCount = 0
    for i in range(len(testing_set)):
        if testing_labels[i] != predicted_labels[i]:
            errorCount += 1
    errorRate = float(errorCount) / len(testing_set)
    print "Error Rate of Decision_Tree Classifier: " + str(errorRate)
    #


    # #Given new Query, Return classification of Query
    result = classifier.predict(query)
    #print "Query Classified as: " + str(result)
    return result

main(InputFileName, "Test")

