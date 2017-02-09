import json
from flask import request
from flask import Flask
import sys, os
from binary_classifier_CNN import bcCNN

def usage_message():
    print "This script connects bCNNs to the endpoint host (i think)"
    print "Usage: python app.py [-m=<module names>]"
    exit()

log('running')

args = sys.argv[1:]

if len(args) < 1:
    usage_message()

trained_models = args[0]

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    filepath = request.get_json()["file_path"]

    # model_path = "./classifiers/formal/"
    # changed from above to accomodate multiple
    model_paths = []
    for model in trained_models:
        model_paths.append("./classifiers/"+model+"/")
    print model_paths

    # formal_net = bcCNN.Net(model_path)
    # changed from above to accomodate multiple
    classifications = []
    for path in model_paths:
        model_net = bcCNN.Net(path)
        classification = model_net.classify(filepath)
        if classification == 1:
            classifications.append(path[14:-1])
        else:
            classifications.append("not" + path[14:-1])
        print classifications
    classifications_dict = dict(zip(trained_models,classifications))

    #dictionary = { "classification" : classification }
    result = json.dumps(classifications_dict)

    return result

app.run(debug=True)
# app.run(host="0.0.0.0")
