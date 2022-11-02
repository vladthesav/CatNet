import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

import sys
import os 

from reddit_data_ingestion import * 

s3 = boto3.client('s3')


def handler(event, context):
    #check if API client id/secret keys are provided 
    if "client_id" not in event: raise Exception("Error: reddit praw API client id not provided")  
    if "client_secret" not in event: Exception("Error: reddit praw API secret id not provided")  

    client_id = event["client_id"]
    client_secret = event["client_secret"]

    #make praw client
    reddit_read_only = praw.Reddit(client_id=client_id, client_secret=client_secret,user_agent = "idk")

    #get other params
    limit_per_subreddit = event["limit"] if "limit" in event else 50 

    #testing reddit api 
    s=get_img_urls_from_subreddit("mainecoons", client=reddit_read_only, limit=limit_per_subreddit) 
    print(s)

    #upload data to s3 
    s3.put_object(Body="testing testing 123", Bucket='cat-breed-data', Key='test.txt')

    

    return 'Hello from AWS Lambda using Python' + sys.version + '!'        