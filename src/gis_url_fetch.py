import os
from PIL import Image
from google_images_download import google_images_download

gid = google_images_download.googleimagesdownload()

search_queries = ["trains"]


def downloadimages(query):
    arguments = {"keywords": query,
                 # "format": "jpg",
                 "limit": 100,
                 "print_urls": True,
                 # "size": "large"
                 "exact_size": "1920, 1080"
                 }
    try:
        gid.download(arguments)

    except FileNotFoundError:
        arguments = {"keywords": query,
                     # "format": "jpg",
                     "limit": 4,
                     "print_urls": True,
                     "size": "medium"}

        # Providing arguments for the searched query 
        try:
            # Downloading the photos based 
            # on the given arguments 
            gid.download(arguments)
        except:
            pass


def clean_corrupt_images(img_dir):
    for filename in os.listdir(img_dir):
        try:
            with Image.open(img_dir + "/" + filename) as im:
                print('ok')
        except:
            print(img_dir + "/" + filename)
            os.remove(img_dir + "/" + filename)


if __name__ == "__main__":
    for query in search_queries:
        downloadimages(query)

    clean_corrupt_images("./downloads")
