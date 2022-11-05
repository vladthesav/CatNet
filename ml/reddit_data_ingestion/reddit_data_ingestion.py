from PIL import Image
import requests
from io import BytesIO
import praw


def get_img(url):
  res = requests.get(url)
  if res.status_code!=200: return None 
  img = Image.open(BytesIO(res.content)).convert("RGB")
  return img 


def parse_gallery(gallery, max_h=900, max_w=900):
  #parse submission object for gallery
  #to get list of urls 

  #INPUT 
  #gallary = submission object that points to gallary 

  #OPUTPUT
  #urls = list of image urls 

  if not hasattr(gallery, "media_metadata"): return None 

  #get post metadata
  metadata = gallery.media_metadata
  
  #get gallary pages that look ok
  pages = [metadata[page]["p"] for page in metadata if metadata[page]["status"]=="valid" and metadata[page]["e"]=="Image"]

  #for each page, get image which isn't too big 
  urls = []
  #each of these has a list of the same image in differetn sizes
  #since they are sorted, we will grab the largest image that fits within out bounds
  for img_sizes in pages:
    url =None
    for img in img_sizes:
      if img["x"] <= max_w and img["y"] <= max_h: url = img["u"]
    if url!=None: urls.append(url)
  return urls



def get_img_urls_from_subreddit(subreddit, client=None, limit=50000):
  #get list of image urls from subreddit

  #get submissions
  subreddit = client.subreddit(subreddit).top("all",limit=limit)
  
  #get submission urls 
  submissions = [s for s in subreddit if "i.redd.it" in s.url or "/gallery/" in s.url]

  img_urls = []

  for submission in submissions:
    url=submission.url
    if "i.redd.it" in url:
      img_urls.append(url)
    elif "/gallery/" in url:
      gallary_img_urls =  parse_gallery(submission)
      #don't add to urls list if we cant parse
      if gallary_img_urls==None: continue
      for u in gallary_img_urls(submission):
        try:
            img_urls.append(u)
        except Exception as e: 
            print(e)
            
  return img_urls


cat_breed_subreddits =[("abyssinian","Abyssinians"), ("bengal","bengalcats"), ("birman","birmans"),
                       ("bombay","BombayCat"),("british_shorthair","britishshorthair"),
                       ("egyptian_mau","egyptianmau"), ("maine_coon","mainecoons"), ("persian", "persiancat"), 
                       ("ragdoll","ragdolls"),("russian_blue","russianblue"),("siamese","Siamesecats"), ("sphynx","sphynx")]

class_subreddit_mapping = {c:subreddit for c,subreddit in cat_breed_subreddits}