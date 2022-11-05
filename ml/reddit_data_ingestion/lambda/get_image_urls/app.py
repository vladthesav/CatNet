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
    if "cat_breed" not in event: Exception("Error: cat breed not provided")  

    client_id = event["client_id"]
    client_secret = event["client_secret"]
    cat_breed = event["cat_breed"]

    if cat_breed not in class_subreddit_mapping: return Exception("Error: {} not recognized cat breed".format(cat_breed))
    cat_breed_subreddit = class_subreddit_mapping[cat_breed]

    print("scraping {}...".format(cat_breed_subreddit))
    #make praw client
    reddit_read_only = praw.Reddit(client_id=client_id, client_secret=client_secret,user_agent = "idk")

    #get other params
    limit_per_subreddit = event["limit"] if "limit" in event else 50


    cat_breed_urls = ""

    #get cat pic urls for that subreddit
    urls=get_img_urls_from_subreddit(cat_breed_subreddit, client=reddit_read_only, limit=limit_per_subreddit) 

    #add url and cat breed type to output file
    for url in urls: cat_breed_urls += "{} {}\n".format(url, class_name)


    output_s3_path = 'reddit/cat_pic_urls_max_{}_per_subreddit.txt'.format(limit_per_subreddit) 

    #upload cat pic urls to s3
    s3.put_object(Body=cat_breed_urls, Bucket='cat-breed-data', Key=output_s3_path)

    

    return "cat pic urls saved to : " + output_s3_path      