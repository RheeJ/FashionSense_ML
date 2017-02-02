import json
from flask import request
from flask import Flask
import os
from binary_classifier_CNN import bcCNN


app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():

    filepath = request.get_json()

    # classification = bcCNN.Net().classify(filepath)
    classification = "formal"

    dictionary = { "classification" : classification }
    result = json.dumps(dictionary)

    return result

# #app.run(debug=True)
# app.run(host="0.0.0.0")
