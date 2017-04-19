import sqlite3
import os
import utils
import boto3
import shutil

classified_images = {}
classifiers = utils.get_classifiers()

for image_path in list(os.walk("./images"))[1:]:

    classifications = utils.get_classifications(classifiers, image_path)
    classified_images[image_path] = classifications
