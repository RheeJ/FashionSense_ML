import boto3
import sys, os
from os import listdir
from os.path import isfile, join

def usage_message():
    print "This script allows you to upload files to the aws buckets!"
    print "Usage: python boto.py [-f=<file to upload>][-b=<bucket name>] optional: [-s=bucket folder]"
    exit()

# Get inputs
args = sys.argv[1:]
if len(args) < 2:
    usage_message()
elif len(args) == 3:
    pathname = args[0]
    bucket = args[1]
    sub_bucket = args[2]
else:
    pathname = args[0]
    bucket = args[1]
    sub_bucket = False


# Shortening the s3 command, nothing special
s3 = boto3.resource('s3')

# Confirm file or directory path exists/check if directory
if os.path.isfile(pathname):
    print "Uploading file " + pathname
    directory = False
elif os.path.isdir(pathname):
    print "Uploading file" + pathname
    directory = True
else:
    print "Sorry, I couldn't find that file"
    os._exit(1)

# Confirm bucket exists
from botocore.client import ClientError
bucket = s3.Bucket(bucket)
print "Now accessing bucket " + bucket.name
exists = True
try:
    s3.meta.client.head_bucket(Bucket=bucket.name)
    print "Bucket found!"
except ClientError:
    # The bucket does not exist or you have no access.
    print "Bucket not found"
    os._exit(2)

# If dirctory, get a list of files (can't do nested directories yet)
if directory:
    files = [f for f in listdir(pathname) if isfile(join(pathname, f))]
    print type(files)
    print "Including files:"
    for item in files:
        print item
else:
    files = pathname

# Smaller than 5GB upload
#s3_connection = boto3.connect_s3()
#bucket = s3.get_bucket(bucket)
for item in files:
    print item
    if directory:
        name = pathname+"/"+item
    elif sub_bucket != False:
        name = sub_bucket+"/"+item
    else:
        name = item
    print "Now uploading "+name
    data = open(name, 'rb')
    s3.Bucket(bucket.name).put_object(Key=name, Body=data)
print "Uploading complete!"

# Larger than 5GB upload
