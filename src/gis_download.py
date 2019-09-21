import urllib.request as ur
import numpy as np
from google_images_search import GoogleImagesSearch

key = "AIzaSyAsUTxqRNuMVuGFGFfchQ6B6H-dN6Z2N00"
cx = "006445825262294488104:kmw8up7owiw"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}

gis = GoogleImagesSearch(key, cx)

_search_params = {
    'q': 'cats',
    'num': 100,
    'safe': 'off',
    'fileType': 'jpg',
    # 'imgType': 'clipart|face|lineart|news|photo',
    'imgSize': 'huge',
    # 'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow'
}

# this will only search for images:
gis.search(search_params=_search_params)
print(gis.results())

for x in gis.results():
    req = ur.Request(x._url, None, headers)
    try:
        res = ur.urlopen(req)
    except:
        print("FAILED TO DOWNLOAD")
    image = np.asarray(bytearray(res.read()), dtype='uint8')
    print(image)

# # this will search and download:
# gis.search(search_params=_search_params, path_to_dir='./downloads')
#
# # this will search, download and resize:
# gis.search(search_params=_search_params, path_to_dir='./downloads', width=500, height=500)
#
# # search first, then download and resize afterwards
# gis.search(search_params=_search_params)
# for image in gis.results():
#     image.download('./downloads')
#     print('downloaded an image')
#     image.resize(500, 500)