###By: Jimmy Song
###Decision Tree for Fashion-Style Classification

import sys
import pickle
from sklearn import tree

InputFileName = str(sys.argv[1])
Query = str(sys.argv[2])

def preprocess(filename):
    #TODO: Preprocess input file once images have been scraped.
    pass

def save_classifier(classifier, training_set, training_labels):
    pickle.dump(classifier, open('classifier_1.p', 'w'))
    pickle.dump(training_set, open('training_set_1.p', 'w'))
    pickle.dump(training_labels, open('training_labels.p_1', 'w'))

def main(filename, query):
    training_set, training_labels = preprocess(filename)

    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(training_set, training_labels)
    save_classifier(classifier, training_set, training_labels)
    classifier = pickle.load(open('classifier_1.p'))
    result = classifier.predict(query)

    print result
    return result

main(InputFileName)
