import json
import tempfile
from flask import request
from flask import Flask
from flask import abort
import sys, os
from binary_classifier_CNN import bcCNN
from utils import get_classifications
from utils import get_classifiers


# get trained models
classifers = get_classifiers()

def get_classifications_wrapper(temp_file):
    return get_classifications(classifers, temp_file)

# webapp
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
    classifications_dict = get_classifications_wrapper(temp)

    # close temp file
    temp.close()

    result = json.dumps(classifications_dict)
    return result

if __name__ == "__main__":

    # if you want to run in debug set the environment variable in teminal
    # $ export DEBUG=1
    debug = os.environ.get('DEBUG')
    if debug:
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
