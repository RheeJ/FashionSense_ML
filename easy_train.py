import sys, os
import boto3

def download(bucket, foldername, polarity):
    # Confirm dest directory exists
    dest = "images/"+polarity
    if not(os.path.isdir(dest)):
        os.makedirs(dest)
    # Confirm bucket exists
    bucket = s3.Bucket(bucket)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket.name)
    except ClientError:
        # The bucket does not exist or you have no access.
        print "Bucket not found"
        os._exit(0)
    prefix = foldername+"/"
    items = []
    for obj in bucket.objects.filter(Prefix=prefix):
        items.append(obj)
        target = obj.key
        try:
            s3.Object(bucket.name, target).get()
        except ClientError:
            print "Target "+target+" not found"
            # The target is unidentified
            os._exit(1)
        name = target.split("/")
        type(name)
        name = name[len(name)-1]
        s3.meta.client.download_file(bucket.name, target, dest+"/"+name)
    print foldername + " folder download complete!"

if __name__ == "__main__":
    positives = sys.argv[1]
    negatives = []
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket='imagedataset', Delimiter='/'):
        for prefix in result.get('CommonPrefixes'):
            negatives.append(prefix.get('Prefix'))

    download("imagedataset", positives, "positive")
    for folder in negatives:
        download("imagedataset", folder, "negative")
