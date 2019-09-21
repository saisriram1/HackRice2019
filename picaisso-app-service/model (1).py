#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch
import torchvision.models as models
import torch.optim as optim
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import os
import numpy as np
# Required inputs:
num_classes = 2
num_epochs = 100

# Define model:
model = models.resnet50(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, num_classes)  # modify output layer to only have num_classes outputs
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)  # send model to GPU

# Define optimizer:
optimizer = optim.Adam(model.parameters())  # define SGD optimizer

# Define loss function:
loss_fxn = nn.CrossEntropyLoss()

# Set up Tensorboard logging to ./runs/:
writer = SummaryWriter()

# ----- Obtain Training Data -----
class DatabaseDataset(Dataset):
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
            correct = torch.tensor(0.0, dtype=torch.long)
        else:
            correct = torch.tensor(1.0, dtype=torch.long)
        sample = {"image": inputTensor, "class": correct}
        return sample
    
    def __len__(self):
        return len(self.all_imgs)

dogs_and_cats_train = DogsandCatsDataset("./train/", im_size=224)
trainloader = DataLoader(dogs_and_cats_train, batch_size=8, shuffle=True, num_workers=2)

dogs_and_cats_val = DogsandCatsDataset("./val/", im_size=224)
valloader = DataLoader(dogs_and_cats_val, batch_size=1, shuffle=True, num_workers=2)

# Training loop:
for epoch in range(num_epochs):
    running_loss = 0.0
    for phase in ["val", "train"]:
        if phase == "train":
            model.train(True)
            loader = trainloader
        else:
            model.train(False)
            loader = valloader
            num_correct = 0.
        for ibatch, data in enumerate(loader, 0):
            inputs = data["image"]  # batch size x 3 x image_height x image width
            correct_output = data["class"]
            inputs, correct_output = inputs.to(device), correct_output.to(device)  # send inputs and labels to the GPU
            optimizer.zero_grad()  # make sure gradients are zeroed
            actual_output = model(inputs)  # forward pass
            if phase == "train":
                loss = loss_fxn(actual_output, correct_output)  # compute loss
                loss.backward()  # backpropagate the loss
                optimizer.step()  # update weights
                writer.add_scalar('data/trainingloss', loss, ibatch)  # record loss in tensorboard
                running_loss += loss.item()

            # print statistics
            printevery = 200
            if (ibatch % printevery == printevery-1) and (phase == "train"):  # print every 200 mini-batches
                print('[%d, %5d] loss: %.3f' % (epoch + 1, ibatch + 1, running_loss / printevery))
                running_loss = 0.0
            elif phase == "val" :
                correct_idx = np.max(correct_output.cpu().detach().numpy())
                idx = np.argmax(actual_output.cpu().detach().numpy())
                if correct_idx == idx:
                    num_correct += 1.
#                 if ibatch < 5:
#                     im1 = np.swapaxes(inputs.squeeze().cpu().numpy(), 0, 2)
#                     imgplot = plt.imshow(im1)
#                     if idx == 1:
#                         txt = "cat"
#                     else:
#                         txt = "dog"
#                     plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
#                     print("correct output, prediction", correct_idx, idx)
                if ibatch == len(loader) - 1:  # only print val loss once, after all images have been computed
                    print("num correct, total", num_correct, len(loader))
                    print("val accuracy:", num_correct / len(loader))
                
print("Finished Training")


# In[ ]:




