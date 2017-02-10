import json
import tempfile
from flask import request
from flask import Flask
from flask import abort
import sys, os
from binary_classifier_CNN import bcCNN
from app_utils import get_classifications

app = Flask(__name__)
@app.route('/', methods=['POST'])

def index():

    data = request.get_data()
    temp = tempfile.TemporaryFile()
    temp.write(data)
    temp.seek(0)
    classifications_dict = get_classifications(temp)
    result = json.dumps(classifications_dict)
    temp.close()

    if data == None:
        abort(400)

    return result

if __name__ == "__main__":

    debug = os.environ.get('DEBUG')
    if debug:
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
