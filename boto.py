import boto3
import sys, os
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def usage_message():
    print "This script allows you to upload files to the aws buckets!"
    print "Usage: python boto.py [-f=<file to upload>][-b=<bucket name>]"
    exit()

# Get inputs
if len(args) < 2:
    usage_message()
else:
    pathname = args[0]
    bucket = args[1]

# Shortening the s3 command, nothing special
s3 = boto3.resource('s3')

# Confirm file or directory path exists/check if directory
if os.path.isfile(pathname):
    print "Uploading file " + pathname
elif os.path.isdir(pathname):
    directory = False
    print "Uploading file" + pathname
    directory = True
else:
    print "Sorry, I couldn't find that file"

# Confirm bucket exists
for bucket in s3.buckets.all():
    print "Now accessing bucket " + bucket
bucket = s3.Bucket(bucket)
exists = True
try:
    s3.meta.client.head_bucket(Bucket=bucket)
    print "Bucket found!"
except botocore.exceptions.ClientError as e:
    print "Bucket not found"
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

# If dirctory, get a list of files (can't do nested directories yet)
if directory:
    files = [f for f in listdir(pathname) if isfile(join(pathname, f))]
    print files
else:
    files = pathname

# Smaller than 5GB upload
s3_connection = boto.connect_s3()
bucket = s3_connection.get_bucket(bucket)
for this_file in files
    if directory:
        name = directory+this_file
    else:
        name = this_file
    print "Now uploading "+name
    key = boto.s3.key.Key(bucket, name)
    with open(name) as f:
        key.send_file(f)
print "Uploading complete"

# Larger than 5GB upload
