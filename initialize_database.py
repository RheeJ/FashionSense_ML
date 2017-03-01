import sqlite3
import os
import utils


conn = sqlite3.connect('database/database.db')
c = conn.cursor()

# generate table description based on model
table_description = "CREATE TABLE images (image_path text,"
categories = []
for model_path in list(os.walk("./classifiers"))[1:]:
    category = model_path[0].split('/')[2]
    categories.append(category)
    table_description += (' ' + category + " integer  ,")
table_description = table_description[:-1]
table_description += ')'

# create the table
c.execute(table_description)

# TODO: run bcCNN on all images and get the classifications
"""
I would probably just create a default image directory (i.e. ./images)
that contains all the images and then run the get_classifiers and get_classifications functions
(inside utils) to get all the classifications. Then you will be able to use that to insert into the database
using the command below
"""
classifiers = utils.get_classifiers()
for image_path in list(os.walk("./images"))[1:]:

    insert_string = "INSERT INTO images VALUES ( " + image_path + ','
    classifications = get_classifications(classifiers, image_path)
    for cat in categories:
        insert_string += (' ' + cat  + ',')
        c.execute(insert_string)
    insert_string += ' )'
    c.execute(insert_string)

conn.commit()
conn.close()
