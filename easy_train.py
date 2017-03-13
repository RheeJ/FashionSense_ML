import os
import boto3
import boto


if __name__ == "__main__":

# Get inputs
    folder = sys.argv[1]
    boto.download_in("imagedataset", folder, positives)

    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket='edsu-test-bucket', Delimiter='/'):
        for prefix in result.get('CommonPrefixes'):
            print(prefix.get('Prefix'))
