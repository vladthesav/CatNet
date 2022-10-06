import torch 
from torchvision import  transforms

import numpy as np 
from PIL import Image 

#set device for pytorch 
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("using {} as device".format(device))

#list of class names 
_cat_breed_list = ["abyssinian", "bengal", "birman", "bombay", "british_shorthair", "egyptian_mau", "maine_coon", "persian", "ragdoll", "russian_blue", "siamese","sphynx"]


#transforms needed to prepare image for model
tfms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

#load model 
print("loading model...")
net = torch.load("model.pt").to(device).eval()

def softmax(x):
    #numerically stable softmax
    b = x.max()
    x = x-b 
    exp_x = np.exp(x)

    return exp_x/np.sum(exp_x)

#cat breed prediction pipeline 
def predict_cat_breed(image, net=net, tfms =tfms, class_names = _cat_breed_list):
    #run PIL image through ML pipeline 

    #INPUTS 
    #image = PIL image we want to predict 
    #net = neural net we want to use 
    #tfms = transforms needed to prepare image for net 
    #class_names = name associated with each class index

    #OUTPUT 
    #output of model 

    #step one - prepare data for model 
    x = tfms(image).to(device)
    x=x.unsqueeze(dim=0)

    #step two - run through model 
    with torch.no_grad(): y_hat = net(x)

    #put output back into cpu 
    y_hat = y_hat.to("cpu")

    #get rid of extra dim and turn into numpy array 
    y_hat = y_hat[0].numpy()

    #apply softmax because people like to see percents 
    y_hat = softmax(y_hat)*100

    #turn this into list of tuples containing class name 
    preds = [(cname, conf) for cname, conf in zip(class_names, y_hat)]

    #sort by model confidence
    preds = sorted(preds, key = lambda x: x[1], reverse = True)

    #turn percents into strings so we can serialize as json 
    preds_serializable = [(cname, str(conf)[:5]) for cname, conf in preds]
    return preds_serializable




#test ml pipeline on image 
#fpath = "maine-coon.jpg"
#test_img = Image.open(fpath)
#out = predict_cat_breed(test_img)
#print(out)