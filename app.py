import json
from flask import request
from flask import Flask
import os
from binary_classifier_CNN import bcCNN

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    filepath = request.get_json()["file_path"]

    model_path = "./classifiers/formal/"
    formal_net = bcCNN.Net(model_path)
    classification = formal_net.classify(filepath)

    if classification == 0:
        classification = "formal"
    else:
        classification = "not formal"

    dictionary = { "classification" : classification }
    result = json.dumps(dictionary)

    return result

# #app.run(debug=True)
# app.run(host="0.0.0.0")
