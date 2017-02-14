import boto3

s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print "Now accessing: "(bucket.name)


bucket = s3.Bucket('imagedataset')
exists = True
try:
    s3.meta.client.head_bucket(Bucket='imagedataset')
except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False
