import numpy as np
from PIL import Image
import io
import os
from io import BytesIO
import base64
import requests
import tempfile
from fnvhash import fnv1a_64
from timeit import default_timer as timer


def persist_images(conn, urls):
    """ Save images to an external database."""
    func_start_time = timer()
    print('Persisting found images')
    num_embedded = 0
    num_urls = 0
    # Write urls in batches
    for index, url in enumerate(urls):
        if not url:
            continue
        start_time = timer()
        if is_base64_encoded(url):
            img_np_array = prepare_base64_image(url)
            num_embedded += 1
        elif url[:4] == 'http':
            img_np_array = read_convert_image_from_url(url)
            num_urls += 1
    print('Number of embedded images: {}'.format(num_embedded))
    print('Number of links: {}'.format(num_urls))
    print('Done in {:.2f}s'.format(timer() - func_start_time))


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
    img_bytes_np_array = convert_bytes_to_numpy(img_bytes)
    return img_bytes_np_array


def convert_bytes_to_numpy(img_bytes):
    """ Convert an image (as BytesIO in-memory buffer) to Numpy array. """
    # Rewind to beginning of buffer, so PIL can read it
    img_bytes.seek(0)
    # Open the image via PIL and read into a Numpy array
    img_np_array = np.array(Image.open(img_bytes).convert('RGB'))
    return img_np_array


# def read_convert_image_from_url(url):
#     """ Read the image and convert it to Numpy array. """
#     # Get the image as in memory file-like object
#     response = requests.get(url, stream=True)
#     img_bytes = BytesIO(response.content)
#     return convert_bytes_to_numpy(img_bytes)


def convert_bytes_to_jpeg(img_bytes):
    """ Convert an image (as BytesIO in-memory buffer) to JPEG. """
    # Convert to another file-like buffer but in JPEG format
    img_bytes_converted = BytesIO()
    img_bytes.flush()
    # Rewind to beginning of buffer, so PIL can read it
    img_bytes.seek(0)
    Image.open(img_bytes).convert('RGB').save(
        img_bytes_converted, format='JPEG')
    img_bytes_converted.seek(0)
    return img_bytes_converted


def read_convert_image_from_url(url):
    """ Read the image and convert it to JPG. """
    # Get the image as in memory file-like object
    response = requests.get(url, stream=True)
    img_bytes = BytesIO(response.content)
    return convert_bytes_to_jpeg(img_bytes)


def save_image(url, download_dir):
    """ Download the image and save. """
    r = requests.get(url, stream=True)
    # print(convert_bytes_to_numpy(BytesIO(r.content)))
    data = read_convert_image_from_url(url)
    hashed = str(fnv1a_64(url.encode('utf-8')))
    filename = hashed + '.jpeg'
    key = os.path.join(download_dir, filename)
    with open(key, 'wb') as f:
        f.write(data.read())
