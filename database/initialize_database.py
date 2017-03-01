import sqlite3
import os


conn = sqlite3.connect('database.db')
c = conn.cursor()

# generate table description based on model
table_description = "CREATE TABLE images (image_path text,"
for model_path in list(os.walk("../classifiers"))[1:]:
    category = model_path[0].split('/')[2]
    table_description += (' ' + category + ' integer ' ',')
table_description = table_description[:-1]
table_description += ')'

# create the table
c.execute(table_description)

# TODO: run bcCNN on all images and get the classifications
"""
I would probably just create a default image directory (i.e. ../images)
that contains all the images and then run the get_classifiers and get_classifications functions
(inside utils) to get all the classifications. Then you will be able to use that to insert into the database
using the command below
"""
# c.execute("INSERT INTO images ... ")

conn.commit()
conn.close()
