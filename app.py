import json
import tempfile
from flask import request
from flask import Flask
from flask import abort
from flask import send_file
import sys, os
from binary_classifier_CNN import bcCNN
from utils import get_classifications
from utils import get_classifiers
import sqlite3
from flask import g


# get trained models
classifers = get_classifiers()

def get_classifications_wrapper(temp_file):
    return get_classifications(classifers, temp_file)


# webapp
app = Flask(__name__)


DATABASE = './database/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/classify', methods=['POST'])
def classify():

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


@app.route('/classifications', methods=['GET'])
def classifications():

    categories = []
    # TODO: pull out classifications iteration into utils
    for path in list(os.walk("./classifiers"))[1:]:
        model_path = path[0]
        category = model_path.split('/')[2]
        categories.append(category)

    result = json.dumps({ "categories" : categories})
    return result


# TODO: implement endpoint that returns images
# with specific classification
@app.route('/classified', methods=['GET'])
def classified():

    classification = request.args.get('classification')
    if classification == None:
        abort(400)

    db = c = conn.cursor()

    # go through and select all images that have

    # dumby value
    file_name = "./test.jpg"

    return send_file(file_name, mimetype='image/jpeg')


# TODO: implement endpoint which returns
# similar images to one posted
# @app.route('/image', methods=['POST'])
# def images():
#     pass


if __name__ == "__main__":

    # if you want to run in debug set the environment variable in teminal
    # $ export DEBUG=1
    debug = os.environ.get('DEBUG')
    if debug:
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
