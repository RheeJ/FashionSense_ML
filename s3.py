import boto3
import sys, os
from os import listdir
from os.path import isfile, join
from botocore.client import ClientError

s3 = boto3.resource('s3')
client = boto3.client('s3')

def usage_message():
    print "This script communicates with aws S3 buckets"
    print "First argument must be either: -up or -down"
    exit()

def up_usage_message():
    print "Usage: python boto.py -up <object to upload> <bucket name> optional: <bucket folder>"
    exit()

def down_usage_message():
    print "Usage: python boto.py -down <object to download> <bucket name> <download destination>"
    print "Example: 'python boto.py -down imagedataset/beach/0.jpg imagedataset images/0.jpg' will save the first image in the beach folder from the imagedataset bucket to a file called 0.jpg in the directory images within your current working directory"
    exit()

def download(bucket, sub_bucket = null, folder = null, filename = null, dest = null):
    """
    bucket (str): bucket name to download from
    sub_bucket (str): (optional) sub bucket within bucket to download from
    folder (str): (optional) folder within bucket to download from. if not specified, entire bucket contents will be downloaded
    filename (str): file to download
    dest (str): local destination to store download. default is current directory. if directory doesn't exist, it is created
    """
    #TODO: implement sub_bucket functionality

    #check directory exists
    if (dest):
        if os.path.isdir(dest):
            print "Saving contents to " + dest
        else:
            print "Couldn't find the specified destination. Creating..."
            try:
                os.makedirs(dest)
            except:
                print "Couldn't create the specified destination"
                exit()
    else:
        print "Saving contents to current directory"

    #Confirm bucket exists
    try:
        bucket = s3.Bucket(bucket)
        print "Now accessing" + bucket.name
    except:
        print "Couldn't access specified bucket"
        exit()

    try:
        s3.meta.client.head_bucket(Bucket = bucket.name)
        print "Bucket found"
    except ClientError:
        print "Bucket not found"
        os.exit(2)

    #Download
    items = []
    if folder and not filename:
        for obj in bucket.objects.filter(folder):
            target = str(obj.key)
            print "Downloading" + target
            try:
                s3.Objet(bucket.name,target).get()
            except:
                print "Couldn't download" + target


if __name__ == "__main__":

# Get inputs
    args = sys.argv[1:]
    method = args[0]
    if method == "-down":
        if len(args) != 4:
            down_usage_message()
        else:
            pathname = args[1]
            bucket = args[2]
            dest = args[3]

    elif method == "-up":
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

    elif method == "-down_in":
        if len(args) == 3:
            bucket = args[1]
            folder = args[2]
    else:
        usage_message()

# Choosing which to run
    if method == "-down":
        print "Downloading beginning"
        download(bucket, pathname, dest)
    # 
    # elif method == "-up":
    #     print "Uploading beginning"
    #     upload(pathname, bucket, sub_bucket)

    else:
        print "No correct method found, exiting program"
        exit()
