import sys
from reddit_data_ingestion import * 


def handler(event, context):
    #check if API client id/secret keys are provided 
    if "client_id" not in event: raise Exception("Error: reddit praw API client id not provided")  
    if "client_secret" not in event: Exception("Error: reddit praw API secret id not provided")  

    client_id = event["client_id"]
    client_secret = event["client_secret"]

    #make praw client
    reddit_read_only = praw.Reddit(client_id=client_id,  
                               client_secret=client_secret,
                               user_agent = "idk")

    

    return 'Hello from AWS Lambda using Python' + sys.version + '!'        