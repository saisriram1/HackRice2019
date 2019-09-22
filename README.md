# picaisso.
Two central problems in AI are 1) the **lack of scalable datasets**, and 2) the **sheer amount of knowledge and resources someone needs to build a model**. Picaisso targets these problems simultaneously by taking care of dataset collection and model training for you. Picaisso will compute a suitable dataset to train a general-purpose deep-learning classifier for any two classes you want. Better yet, Picaisso will **provide you with the dataset of images from the two classes as well as the classifier itself**. We automate everything; it's as simple as typing the classes you want to distinguish between. **Classification simplified.**

## Stack 

* React
* Express.js 
* Node.js 
* Python 
  * Flask 
  * Selenium 
  * PyTorch 
* Google Compute Engine 


## Requirements 
Because this project relies on ChromeDriver, you must have Chrome v77 installed in the default location on your machine. To run the picaisso-scraper-service, you also need Python 3.7. 

## Project Overview
This repo contains three directories corresponding to the three services of picaisso. 

1. The **picaisso-app-service** directory contains the code for the client-facing web application. It has a front-end built in React with a backend in Express.js and Node.js. Because the Node server runs locally, you would need some other third-party service to open it up to the general web (we've been using ngrok). 

2. The **picaisso-scraper-service** is a Flask service that handles the web scraping of images to build the dataset. Its primary point of entry is the /picassio endpoint, which is reached by the picaisso-app-service whenever a user submits a new request. Upon making a POST request to the /picassio endpoint, the picassio-scraper-service runs through a workflow that scrapes images to build the dataset, posts the URLs to an external MySQL database, makes other requests to inform the picaisso-model-service when to fetch data and begin learning, then emails the zipped dataset and model to the user once both have finished compiling. To start up the service, navigate to the root directory and run app.py.

3. The **picaisso-model-service** is a local version of the model learning service running on Google Cloud's Compute Engine. We use the PyTorch deep learning framework to classify images. We can easily extend our DL backend to classify any number of image classes. As for the specific model architecture, we use PyTorch's ResNet50 architecture pretrained on the 1000 class ImageNet dataset, which is an industry-standard for classification. This service is split into two modes: train and inference. For training, we found that models typically converge within 100 epochs, which takes about 30 minutes to finish. The model file is provided to the user as a set of ResNet50 weights. To instantiate the model on another machine, follow the examples in the inference code. Our inference mode can be run on GPU or CPU (memory permitting), and requires a single image url, which the model will classify.
