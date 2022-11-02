import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

import sys
import os 
import io 

from reddit_data_ingestion import * 

s3 = boto3.client('s3')

#this is bad 
parse_img_id = lambda s: s.split("redd.it/")[1].split(".")[0] 

def upload_img(img, path):
    buffer = io.BytesIO()
    img.save(buffer, "JPEG")
    buffer.seek(0) # rewind pointer back to start
    s3.put_object(
        Bucket='cat-breed-data',
        Key=path,
        Body=buffer,
        ContentType='image/jpeg',
    )

def handler(event, context):
    #get cat pic urls
    if "cat_pic_urls" not in event: raise Exception("Error: cat pic url list not provided")  
    cat_pic_urls = event["cat_pic_urls"]

    # Dget list of cat pic urls
    s3.download_file('cat-breed-data',cat_pic_urls, '/tmp/cat_pics.txt')
    cat_pics = open('/tmp/cat_pics.txt').read().split("\n")

    imgs_uploaded = 0 

    #each line of file is url and class name seperated by space 
    for line in cat_pics: 
        #last line of file is just newline - ignore that
        if " " not in line: break 

        #if not end of file, get cat pic url and breed
        url, breed = line.split(" ")
        print("url={} class={}".format(url, breed)) 

        try:
            img_id = parse_img_id(url)

            img = get_img(url)

            #skip if we can't download url 
            if img==None: continue 

            #try uploading image 
            upload_img(img, "reddit/{}/{}.jpg".format(breed, img_id))

            imgs_uploaded +=1  

        except Exception as e:
            print(e) 


    return "downloaded {} cat pics".format(imgs_uploaded) 