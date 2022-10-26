import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

def get_resnet_base(base_arch, pretrained=True,device=None):
  #get convnet with whatever resnet base archetecture we want
  #with number of output features to help us later

  #INPUTS 
  #base_arch = base archetecture we want as string 
  #pretrained = use pretrained weights or nah 
  #device = device we want to put this on 

  #OUTPUT 
  #base = pytorch model of whatever base arch we want 
  #n_z = number of output features - use this later

  base = None 
  n_z = None 

  #get correct base arch if we have it
  if base_arch=="resnet18":
    base = models.resnet18(pretrained=pretrained) 
    n_z = 512
  elif base_arch =="resnet34":
    base = models.resnet34(pretrained=pretrained) 
    n_z = 512
  elif base_arch=="resnet50":
    base = models.resnet50(pretrained=pretrained) 
    n_z = 2048
  #TODO - ADD MORE LATER!!!!!
  else:
    #can't find it
    return ValueError("Error: unknown base archetecture ",base_arch)

  #put on device we want
  base = base.to(device) if device != None

  #return base arch
  return base, n_z



def make_classifier_head(n_z, n_classes, layers=None):
  #create FC head for classifier 

  #INPUTS 
  #n_z = number of input featues 
  #n_classes = number of classes (output features)
  #layers = if we want layers in between, 
  #         give it a list of output features of each layer
  #device = device we put head on 

  #OUTPUTS 
  #classifier head as pytorch model

  if layers==None:
    return nn.Linear(n_z, n_classes)
  else:
    #TODO - DO STUFF IF WE WANT EXTRA LAYERS
    return


def build_convnet_classifier(base_arch, n_classes, pretrained=True, device=device):
  #build your own convnet classifier with whatever base arch you want

  #INPUTS 
  #base_arch = name of base archetecture we want to use 
  #n_classes = number of things to predict 
  #pretrained = use pretrained weights or nah 
  #device = device we want to put model on 

  #OUTPUT
  #pytorch model with whatever base arch we want 

  #get base archetecture and number of output features 
  #TODO - EXPAND THIS TO OTHER CONVNET ARCHS LIKE VGG/EFFICIENTNET
  base, n_z = get_resnet_base(base_arch, pretrained=pretrained, device=device)

  #set classifier to whatever we need
  classifier_head = make_classifier_head(n_z, n_classes)
  if device != None: classifier_head = classifier_head.to(device)

  #update classifier head
  base.fc = classifier_head 

  return base 



def eval_classifier(net, data_loader, loss_fn, device = torch.device("cpu")):
  #evaluate nn classifier loss/accuracy on valid/test dataset 

  #INPUTS 
  #net = neural net we want to evaluate 
  #data_loader = train/test dataset as dataloader
  #loss_function = loss fn we want to use

  #OUTPUTS
  #acc = validation/test accuracy 
  #loss = validation/test loss 

  running_loss = 0 
  correct = 0 
  n_samples = 0 

  #make sure net is in eval mode
  net.eval()

  for x,y in data_loader:

    n_samples += len(y)

    x=x.to(device)
    y=y.to(device)

    with torch.no_grad(): 
      outputs = net(x)
      sample_loss = loss_fn(outputs, y)

    running_loss += sample_loss.item()

    _, preds = torch.max(outputs, dim = 1) 
    n_correct = (preds == y).sum().item()
    correct += n_correct 

  acc = correct / n_samples
  loss = running_loss/len(data_loader) 

  return acc, loss



def train_model(net, train_loader,valid_loader, loss_fn, optimizer, num_epochs = 25, best_acc=0, device=None ):
  #train neural net

  #INPUTS 
  #net = neural net we want to train 
  #loss_fn = loss function we want to use 
  #optimizer = optimizer used for training
  #num_epochs = number of epochs we want to train for 
  #best_acc = only bother saving weights and updating best_acc if valid acc is better than this 
  #device = device data goes to

  #OUTPUT 
  #best_acc = best accuracy we got, use this when training again to determine whether or not worth saving model

  device = torch.device("cpu") if device==None else device

  best_acc = best_acc  
  best_model_wts = copy.deepcopy(net.state_dict())
  
  for epoch in range(num_epochs):
    #set model to train 
    net.train() 

    running_loss = 0 
    running_correct = 0 
    n_samples = 0 

    #itterate through train loader
    for x,y in train_loader: 
      n_samples += len(y)
      x = x.to(device)
      y = y.to(device)

      #stop optimizer from accumulating gradients 
      optimizer.zero_grad() 

      #calculate loss and accuracy 
      outputs = net(x)
      _, preds = torch.max(outputs, dim = 1) 
      loss = loss_fn(outputs, y)

      #calculate grad
      loss.backward()
      optimizer.step()

      running_loss += loss.item()
      running_correct += torch.sum(preds == y.data)

    train_acc = running_correct / n_samples 
    train_loss = running_loss / len(train_loader)

    print("Epoch {} | train loss: {}  train acc: {}".format(epoch+1, train_loss, train_acc))

    #get validation accuracy and loss  
    valid_acc, valid_loss = eval_classifier(net,valid_loader, criterion ) 

    print("Epoch {} | valid loss: {}  valid acc: {}".format(epoch+1, valid_loss, valid_acc))

    #if best validation acc gets better, save weights
    if valid_acc > best_acc:
      print("validation accuracy increased from {} to {}, saving weights....".format(best_acc, valid_acc))
      best_acc = valid_acc 
      best_model_wts = copy.deepcopy(net.state_dict())
    print('\n')