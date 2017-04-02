import sqlite3
import os
import utils
import boto3
import shutil
'''
# Shortening the s3 command, nothing special
s3 = boto3.resource('s3')
client = boto3.client('s3')
# Pull images from AWS bucket
if not(os.path.isdir("./images")):
    os.makedirs("./images")
bucket = s3.Bucket("imagedataset")

folders = []
paginator = client.get_paginator('list_objects')
for result in paginator.paginate(Bucket="imagedataset", Delimiter='/'):
    for prefix in result.get('CommonPrefixes'):
        tmp = str(prefix['Prefix'])
        folders.append(tmp)
        if not os.path.exists(tmp):
            os.makedirs(tmp)


for aws_object in bucket.objects.all():
    aws_key = aws_object.key
    print aws_key
    print folders
    if aws_key in folders:
        continue     
    dest = "images/"+"-".join(set(aws_key.split("/")))
    s3.meta.client.download_file(bucket.name, aws_object.key, dest)

'''

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

walk = list(os.walk("./images"))
files = walk[0][2]
print files
for file in files:
    image_path = walk[0][0]+file
    insert_string = "INSERT INTO images VALUES ( " + image_path + ','
    classifications = utils.get_classifications(classifiers, image_path)
    for cat in categories:
        insert_string += (' ' + str(classifications[cat])  + ',')
        print "hi"
    insert_string = insert_string[:-1]
    print "hello"
    print insert_string
    insert_string += ' )'
    c.execute(insert_string)

#shutil.rmtree("./images")

conn.commit()
conn.close()

