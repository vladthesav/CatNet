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


    cat_breed_urls = ""

    #get cat pic urls from cat breed subreddits
    for class_name, subreddit in cat_breed_subreddits:
        #get urls 
        urls=get_img_urls_from_subreddit(subreddit, client=reddit_read_only, limit=limit_per_subreddit) 

        #add url and cat breed type to output file
        for url in urls: cat_breed_urls += "{} {}\n".format(url, class_name)


    output_s3_path = 'reddit/cat_pic_urls_max_{}_per_subreddit.txt'.format(limit_per_subreddit) 

    #upload cat pic urls to s3
    s3.put_object(Body=cat_breed_urls, Bucket='cat-breed-data', Key=output_s3_path)

    

    return "cat pic urls saved to : " + output_s3_path      