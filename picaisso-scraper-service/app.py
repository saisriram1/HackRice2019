from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import zipfile
import os

from src.image_scraper import scraper, scraper_io


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello, world!"


@app.route('/picaisso/', methods=['POST', 'GET'])
def api_post():
    if request.method == 'POST':
        req = request.get_json()
        print(req)
        for query in req.values():
            print(f"Now scraping for query {query}")
            workflow(query)
        return jsonify(req)


@app.route('/picaisso/dataset', methods=['GET'])
def upload_images():
    import shutil
    dir_name = './downloads'
    zip_path = shutil.make_archive('./dataset', 'zip', dir_name)
    return send_file(zip_path)


@app.route('/picaisso/model', methods=['GET'])
def upload_model():
    import shutil
    dir_name = './model'
    zip_path = shutil.make_archive('model', 'zip', dir_name)
    return send_file(zip_path)




def workflow(query):
    # Query and scrape all the URLS
    gis = scraper.ImagesScraper()
    urls = gis.get_images(query, max_images=10, fullsize=True)
    gis.cleanup()
    print(urls)

    # Send the URLs to the database
    gis_io = scraper_io.ImageScraperIO()
    gis_io.persist_images(query, urls)


if __name__ == "__main__":
    app.run(debug=True, host='10.126.179.87', port=5000)

