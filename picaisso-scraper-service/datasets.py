#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import torch
from torch.utils.data import Dataset
from torchvision import transforms, utils
from PIL import Image
import torchvision
import torchvision.transforms as transforms

class DogsandCatsDataset(Dataset):
    """
    Class to represent the Dogs and Cats dataset
    """
    def __init__(self, root_dir, im_size=224):
        """
        root_dir: directory with images of cats/dogs
        im_size: integer representing pixel size of image (default 224)
        """
        self.root_dir = root_dir
        self.all_imgs = os.listdir(root_dir)
        self.im_size = im_size
        
    def __getitem__(self, idx):
        """
        idx: the idx^th element of the directory will be returned.
        """
        img_filename = self.all_imgs[idx]  # get the idx^th image filename
        im = Image.open(self.root_dir + img_filename)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),])
        inputTensor = preprocess(im)  # normalize data, resize it, crop it, and convert it to a Tensor
        if img_filename[:3] == "cat":
            correct = torch.Tensor([0., 1.])  # TODO: NOT SURE IF LABEL SHOULD BE 2D OR 1D
        else:
            correct = torch.Tensor([1., 0.])
        sample = {"image": inputTensor, "class": correct}
        return sample

# dataset = DogsandCatsDataset("./data/")
# sample = dataset[1]
# print(sample["image"].shape)
# print(sample["class"].shape)


# In[ ]:




