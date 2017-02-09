import json
from flask import request
from flask import Flask
import sys, os
from binary_classifier_CNN import bcCNN
from app_utils import do_everything
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
    classifications_dict = do_everything(image)
    result = json.dumps(classifications_dict)
    return result

if __name__ == "__main__":

   debug = os.environ.get('DEBUG')
   if debug:
       app.run(debug=True)
   else:
       app.run(host="0.0.0.0")
