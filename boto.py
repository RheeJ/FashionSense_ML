import boto3
import sys, os
from os import listdir
from os.path import isfile, join

def usage_message():
    print "This script communicates with aws buckets!"
    print "Please ensure the first argument is either -up for uploads or -down for downloads"
    exit()

def up_usage_message():
    print "This script allows you to upload files to the aws buckets!"
    print "Usage: python boto.py -up [-f=<file to upload>][-b=<bucket name>] optional: [-s=bucket folder]"
    exit()

def down_usage_message():
    print "This script allows you to download files from the aws buckets!"
    print "Usage: python boto.py -down [-f=<file/folder to download>][-b=<bucket name>][-l=<local destination>]"

# Get inputs
args = sys.argv[1:]
if args[0] == "-up":
    if len(args) != 4:
        up_usage_message()
    else:
        pathname = args[1]
        bucket = args[2]
        dest = args[3]
elif args[0] == "-down":
    if len(args) < 3:
        down_usage_message()
    elif len(args) == 4:
        pathname = args[1]
        bucket = args[2]
        sub_bucket = args[3]
    else:
        pathname = args[1]
        bucket = args[2]
        sub_bucket = False
else:
    usage_message()

print "running"
# Shortening the s3 command, nothing special
s3 = boto3.resource('s3')
client = boto3.client('s3')

# Uploading function
def upload(pathname, bucket, sub_bucket):
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
        print "\nIncluding files:"
        for item in files:
            print item
            print "\n"
        else:
            files = pathname

    for item in files:
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

def download(bucket, file, dest):
    bucket = s3.Bucket(bucket)
    bucket.download_file(file, dest)
    print "File download complete!"

"""
print "Getting list"
listy=client.list_objects(Bucket='imagedataset')['Contents']
print listy[0]
client.download_file('imagedataset', listy[0]['Key'], listy[0]['Key'])

download_dir(client, s3, 'clientconf/', '/tmp')
# Downloading function
def download_dir(client, resource, dist, local='/tmp', bucket='your_bucket'):
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        if result.get('Contents') is not None:
            for file in result.get('Contents'):
                if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):
                     os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))
                resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + file.get('Key'))
"""
