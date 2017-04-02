import json
import tempfile

from flask import Flask
from flask import request
from flask import g
from flask import abort
from flask import send_file
from flask_restful import reqparse
from flask_restful import Resource, Api

import sys, os

from binary_classifier_CNN import bcCNN
from utils import get_classifications
from utils import get_classifiers

import sqlite3

import base64

import utils

app = Flask(__name__)
api = Api(app)

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

def abort_none(returned):
    if returned == None:
        abort(400)

class Classifications(Resource):

    def __init__(self):
        self.classifiers = get_classifiers()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('image', type=str, required=True)

    def post(self):
        """
        passes an image into our models and returns the classifications in JSON
        """

        # get the image hopefully
        args = self.parser.parse_args()

        # decode the image from base64
        image = utils.decode_base64(args["image"])
        abort_none(image)

        # open a temporary image file and run classifications
        classifications = {}
        with utils.create_temporary_image(image) as temp:
            classifications = get_classifications(self.classifiers, temp.name)

        return classifications


class Images(Resource):

    def get(self):

        conn = get_db()
        c = conn.cursor()

        images = { "images": list(c.execute("select * from images")) }

        return images


class Preferences(Resource):

    def get(self):

        return "not implemented"

    def post(self):

        return "not implemented"





# add our endpoints here (just one for now)
base_endpoint = "/v1"

classifications_endpoint = '/'.join((base_endpoint, "classifications"))
images_endpoint = '/'.join((base_endpoint, "images"))

api.add_resource(Classifications, classifications_endpoint )
api.add_resource(Images, images_endpoint)


if __name__ == "__main__":

    debug = os.environ.get('DEBUG')
    if debug:
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
