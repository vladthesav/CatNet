import json, os  
import pandas as pd 
import random 

#cat breeds to look out for 
_cat_breeds_list = ["abyssinian", "bengal", "birman", "bombay", "british_shorthair", "egyptian_mau", "maine_coon", "persian", "ragdoll", "russian_blue", "siamese","sphynx"]
_cat_breeds = set(_cat_breeds_list)


#number of classes
_num_cat_breeds = len(_cat_breeds)

#store mapping between breed name and class index 
_class_idx_mapping = {_cat_breeds_list[i]:i for i in range(_num_cat_breeds)}


#utility functons to get cat pictures and class for each cat pic
def is_cat_breed(path, cat_breeds = _cat_breeds):
  #does this path include name of cat breed?

  #make lowercase so we dont have to deal with caps
  path_lower = path.lower()

  #if file path starts with name of cat breed, then cat breed
  for cat in cat_breeds: 
    if path_lower.startswith(cat): return True 

  #if no cat breed names found, then not cat breed
  return False


def parse_cat_breed(path, cat_breeds = _cat_breeds):
  #if this is a cat breed, get breed from filename

  #whatever breed filename starts with, return that 
  path_lower = path.lower()
  for cat in cat_breeds: 
    if path_lower.startswith(cat): return cat 



def get_cat_pictures(image_folder="images"):
  #given a path to a directory containing oxford pets data,
  #return list of files that contain cat pics 

  #INPUT
  #image_folder = path to oxford pets data 

  #OUTPUT
  #cat_pics = list of paths to cat pics inside that folder 

  #get paths containing cat breed names
  paths = os.listdir(image_folder)
  cat_pics = [path for path in paths if is_cat_breed(path) and ".mat" not in path]

  return cat_pics

def train_val_split(files, p=.8):
  #given a list files, shuffle and split into train and val splits 

  #INPUTS 
  #files = list of files 
  #p = proportion of things we want to go into train, rest go to val 

  #OUTPUTS 
  #train = train split 
  #val = valid split 

  #shuffle data
  random.shuffle(files)

  #get train, val split
  n = len(files)
  n_train = int(p*n)
  n_valid = n-n_train 

  train = files[:n_train]
  val = files[n_train:]

  return train, val



def create_dataframe(cat_pics, image_folder="images"):
  #make a dataframe containing file path, class name, and class index

  #INPUTS 
  #cat_pics = list of files containing cat pics in image_foldr 
  #image_folder = root of cat pics

  #OUTPUT 
  #pandas dataframe containing the info we want 

  rows = []
  for cat_pic in cat_pics:
    fname_lower = cat_pic.lower()
    class_name = parse_cat_breed(fname_lower)
    class_idx = _class_idx_mapping[class_name]
    rows.append({"root":image_folder, "file_path":cat_pic, "class_name":class_name, "class_idx":class_idx})

  return pd.DataFrame(rows)



  