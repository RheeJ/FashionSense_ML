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
import zipfile


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
    """
    classifies image against all the loaded classifiers
    """

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
    """
    returns all classifications that the endpoint serves
    """

    categories = []
    # TODO: pull out classifications iteration into utils
    for path in list(os.walk("./classifiers"))[1:]:
        model_path = path[0]
        category = model_path.split('/')[2]
        categories.append(category)

    result = json.dumps({ "categories" : categories})
    return result


@app.route('/classified', methods=['GET'])
def classified():
    """
    grabs the spefified images with the specified classifications
    """
    # TODO: UNIT TEST THIS SHIT

    # if no classifications specified return nothing
    args = request.args
    if len(args) == 0:
        return json.dumps({})

    # go through the ars and check for num_images and classifications
    num_images = 1
    num_classifications = 0
    query = "select image_path from images where "
    for arg in args:
        if arg == "num_images":
            num_images = args.get(arg)
        else:
            query += (arg + '=' + args.get(arg))
            num_classifications += 1

    if num_classifications == 0:
        return json.dumps({})

    db = get_db()
    c = db.cursor()
    try:
        image_paths = c.execute(query)
    except:
        print "Improper select query"
        print query
    temp_images_zip = "/tmp/images.zip"
    with zipfile.ZipFile(temp_images_zip, 'w') as zipf:
        for ip in image_paths:
            if num_classifications == 0:
                break
            zipf.write(ip[0])
            num_classifications -= 1

    return send_file(temp_images_zip, mimetype="application/zip")


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
