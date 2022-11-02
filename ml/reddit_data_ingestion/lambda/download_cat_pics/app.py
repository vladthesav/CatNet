import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

import sys
import os 

from reddit_data_ingestion import * 

s3 = boto3.client('s3')


def handler(event, context):
    #get cat pic urls
    if "cat_pic_urls" not in event: raise Exception("Error: cat pic url list not provided")  
    cat_pic_urls = event["cat_pic_urls"]

    # Dget list of cat pic urls
    s3.download_file('cat-breed-data',cat_pic_urls, '/tmp/cat_pics.txt')
    cat_pics = open('/tmp/cat_pics.txt.txt').read()

    

    return "downloaded X cat pics" 