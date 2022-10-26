from torchvision import datasets, models, transforms
from torch.utils.data import Dataset, DataLoader
from torchvision import utils

from PIL import Image
import os


#define train and valid transforms here 
train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

valid_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


#write torch dataset for this 
class ImageDataset(Dataset):
  """
    Image dataset

    #INPUTS 
    #df = dataframe containing:
          root = root folder of images (e.g. oxford_pets_data)
          file_path = path to pic within root folder 
          class_idx = index of class 

    #split = which split is this in (train or valid)
  """
  def __init__(self, df, split="valid"):
    #dataframe of paths/labels 
    self.df = df 

    #store dset len here
    self.n_samples = len(df)

    #get correct transform for train/valid splits 
    self.tfm = train_transform if split=="train" else valid_transform 

  def __len__(self): 
    #get number of samples
    return self.n_samples

  def __getitem__(self, idx):
    #get image idx and it's index 
    item_idx = self.df.loc[idx]

    #get image file path 
    root = item_idx["root"]
    fpath = item_idx["file_path"] 
    full_path = os.path.join(root, fpath)

    #get image 
    image = Image.open(full_path).convert('RGB')

    #preprocess/augment image 
    x = self.tfm(image)

    #get class index as well 
    y = item_idx["class_idx"]
    
    return x,y

#get train/valid dataloaders 

def get_image_dataloaders(train_df, valid_df, batch_size=64, num_workers=0):
  #get train and valid dataloader for image data 

  #INPUTS 
  #train_df, valid_df = dataframes where every row contains 
    #a) root folder 
    #b) file path withion that folder 
    #c) class_idx = class index 
  #batch_size = batch size for training 
  #num_workers = num of additional processes for data loading 

  #OUTPUTS 
  #train_loader = dataloader for traing set 
  #valid_loader = dataloader for validation set 

  #get train and valid datsets
  train = ImageDataset(df = train_df, split="train")
  valid = ImageDataset(df = valid_df)

  #get dataloaders

  train_loader = DataLoader(train, batch_size=bs,
                        shuffle=True, num_workers=num_workers)
  valid_loader = DataLoader(valid, batch_size=bs,
                        shuffle=False, num_workers=num_workers)
  
  return train_loader, valid_loader 


