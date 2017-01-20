from app import app
import d_tree
import json
from flask import request

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    f_vector = data['features']
    classified = d_tree.main('int_data.csv', f_vector)
    if classified == 1:
        output = "formal"
    else:
        output = "informal"
    dictionary = { "classification" : output }
    result = json.dumps(dictionary)

    return result
