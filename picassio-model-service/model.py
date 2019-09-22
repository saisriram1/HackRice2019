import torch
import torchvision.models as models
import torch.optim as optim
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from PIL import Image
import numpy as np
import os
import torch
from torchvision import utils
import time
import json
import numpy as np
from io import BytesIO
import base64
import requests
import random
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




# ----------------------------------------- Acquire Training Data Given URLs -----------------------------------------

def persist_images(url):
    """
    Scrape images from website and return PIL Image of that image
    params: url of image to extract
    """
    if is_base64_encoded(url):
        pil_im = prepare_base64_image(url)
    elif url[:4] == 'http':
        pil_im = read_convert_image_from_url(url)
    return pil_im


def is_base64_encoded(data):
    # Base64 encoded images start with 'data:'
    return data[:5] == 'data:'


def prepare_base64_image(data):
    """ Prepate a base64 encode image to be saved. """
    # # Currently all images are JPEG
    # image_type = 'image/jpeg'
    # # From 'image/jpeg' to 'jpeg'
    # image_extension = image_type.replace('image/', '')
    if data[:5] == 'data:':
        # Data is like
        # "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
        # figure the image type and extension
        # image_type = data[data.find("data:"):data.find(";base64")].replace('data:', '')
        # image_extension = image_type.replace('image/', '')
        # The actual base64 encoded image
        data = data[data.find(",") + 1:]
    decoded_image = base64.b64decode(data)
    img_bytes = BytesIO(decoded_image)
    pil_im = convert_bytes_to_PIL(img_bytes)
    return pil_im


def convert_bytes_to_PIL(img_bytes):
    """ Convert an image (as BytesIO in-memory buffer) to PIL Image """
    # Rewind to beginning of buffer, so PIL can read it
    img_bytes.seek(0)
    # Open the image via PIL and read into a Numpy array
    pil_im = Image.open(img_bytes).convert('RGB')
    return pil_im


def read_convert_image_from_url(url):
    """ Read the image and convert it to PIL Image. """
    # Get the image as in memory file-like object
    response = requests.get(url, stream=True)
    img_bytes = BytesIO(response.content)
    return convert_bytes_to_PIL(img_bytes)


# ----------------------------------------- Generate Data for Torch Dataloader -----------------------------------------


def inference(model_file_path, url, num_classes=2):
    """
    Run inference on a pre-trained model/
    :param: model_file_path -- path to the model file
    :param: images -- a list of 1 x 3 x 224 x 224 sized images
    """
    model = models.resnet50(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)  # modify output layer to only have num_classes outputs
    model.load_state_dict(torch.load(model_file_path))
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # model = model.to(device)  # send model to GPU

    model.eval()
    im = persist_images(url)

    preprocess = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(),
                                     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), ])
    inputTensor = preprocess(im)
    inputTensor = torch.unsqueeze(inputTensor, 0)
    # inputTensor.to(device)
    output = model.forward(inputTensor)
    idx = np.argmax(output.cpu().detach().numpy())  # find the actual output

    return str(idx)


@app.route('/inference/', methods=['GET', 'POST'])
def infer():
    if request.method == "POST":
        url = request.get_json()['url']
        return inference('cats_and_dogs.pt', url)


if __name__ == '__main__':
    app.run(debug=True, host='10.126.179.87', port=5050)
