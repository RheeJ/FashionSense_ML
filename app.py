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

    # write binary data to temp file
    data = request.get_data()
    if data == None:
        abort(400)

    temp = tempfile.TemporaryFile()
    temp.write(data)
    temp.seek(0)

    # get the classifications from net
    classifications_dict = get_classifications(temp)

    # close temp file
    temp.close()

    result = json.dumps(classifications_dict)
    return result

if __name__ == "__main__":

    debug = os.environ.get('DEBUG')
    if debug:
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
