import sqlite3
import os
import utils
import boto3
import shutil


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

# Shortening the s3 command, nothing special
s3 = boto3.resource('s3')
client = boto3.client('s3')
# Pull images from AWS bucket
if not(os.path.isdir("./images")):
    os.makedirs("./images")
bucket = s3.Bucket("imagedataset")
#folders = bucket.list("","/")
#names = []
#for i in range(len(folders)):
#    names[i] = folders[i].name
folders = []
paginator = client.get_paginator('list_objects')
for result in paginator.paginate(Bucket="imagedataset", Delimiter='/'):
    for prefix in result.get('CommonPrefixes'):
        folders.append((prefix.get('Prefix')))

print folders
for folder in folders:
    try:
        s3.Object(bucket.name, target).get()
    except ClientError:
        print "Target "+target+" not found"
        os._exit(3)
    for Object in bucket.objects.all():
        # Can be changed to just positive images that we want to categorize
        s3.meta.client.download_file(bucket.name, Object, "./images")

'''
for image_path in list(os.walk("./images"))[1:]:

    insert_string = "INSERT INTO images VALUES ( " + image_path + ','
    classifications = get_classifications(classifiers, image_path)
#images_dir = "./images"
#for image in list(os.walk(images_dir))[0][2]:
#    image_path = images_dir + '/' + image
#   insert_string = "INSERT INTO images VALUES ( '" + image_path + "',"
#    classifications = utils.get_classifications(classifiers, image_path)
    for cat in categories:
        insert_string += (' ' + str(classifications[cat])  + ',')

    insert_string = insert_string[:-1]
    insert_string += ' )'
    c.execute(insert_string)

shutil.rmtree("./images")

conn.commit()
conn.close()
'''
