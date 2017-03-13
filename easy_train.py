# coding: utf-8
import sys, os
import boto3

# Print iterations progress
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(float(bar_length * (iteration / float(total))))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

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
    items = bucket.objects.filter(Prefix=prefix)
    size = sum(1 for _ in items)
    index = 1
    for obj in items:
    #items = []
    #for obj in bucket.objects.filter(Prefix=prefix):
    #    items.append(obj)
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
        s3.meta.client.download_file(bucket.name, target, dest+"/"+name+"1")
        print_progress(index,size)
        index = index+1
    print foldername + " folder download complete!"

if __name__ == "__main__":
    positives = sys.argv[1]
    negatives = []
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket='imagedataset', Delimiter='/'):
        for prefix in result.get('CommonPrefixes'):
            tmp = prefix.get('Prefix')
            if tmp != positives+"/":
                negatives.append(prefix.get('Prefix')[:-1])

    download("imagedataset", positives, "positive")
    for folder in negatives:
        download("imagedataset", folder, "negative")
