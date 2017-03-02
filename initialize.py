import sqlite3
import os
import utils


# TODO: add this to the Dockerfile to run on startup

# TODO: automatically generate classifiers, images and database directories

# TODO: populate the classifiers and images directories

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
try:
    c.execute(table_description)
except:
    print "Database probably alread exists"
    exit()

classifiers = utils.get_classifiers()
images_dir = "./images"
for image in list(os.walk(images_dir))[0][2]:
    image_path = images_dir + '/' + image
    insert_string = "INSERT INTO images VALUES ( '" + image_path + "',"
    classifications = utils.get_classifications(classifiers, image_path)
    for cat in categories:
        insert_string += (' ' + str(classifications[cat])  + ',')

    insert_string = insert_string[:-1]
    insert_string += ' )'
    c.execute(insert_string)

conn.commit()
conn.close()
