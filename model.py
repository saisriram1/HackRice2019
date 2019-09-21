#!/usr/bin/env python
# coding: utf-8

# In[6]:


import torch
import torchvision.models as models
import torch.optim as optim
import torch.nn as nn
import torchvision
from torch.utils.data import DataLoader
from datasets import DogsandCatsDataset
from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import os
test()
a = b

# Required inputs:
num_classes = 2
num_epochs = 10000


# Define model:
model = models.resnet50()
model.fc = nn.Linear(model.fc.in_features, num_classes)  # modify output layer to only have num_classes outputs
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)  # send model to GPU

# Define optimizer:
optimizer = optim.Adam(model.parameters())  # use Adam with default parameters

# Define loss function:
loss_fxn = nn.CrossEntropyLoss()

# Set up Tensorboard logging to ./runs/:
writer = SummaryWriter()

# ----- Obtain Training Data -----
dogs_and_cats = DogsandCatsDataset("./data/", im_size=224)
trainloader = DataLoader(dogs_and_cats, batch_size=4, shuffle=True, num_workers=2)

# Training loop:
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, correct_output = data  # trainloader already splits training data into batches
        inputs, correct_output = inputs.to(device), correct_output.to(device)  # send inputs and labels to the GPU
        optimizer.zero_grad()  # make sure gradients are zeroed
        actual_output = model(inputs)  # forward pass
        loss = loss_fxn(actual_output, correct_output)  # compute loss
        print(loss)
        loss.backward()  # backpropagate the loss
        optimizer.step()  # update weights
        writer.add_scalar('data/trainingloss', loss, i)  # record loss in tensorboard

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:  # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
print("Finished Training")


# In[ ]:




