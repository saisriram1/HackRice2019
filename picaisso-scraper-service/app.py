from flask import Flask, jsonify, request, send_file, redirect, url_for
from flask_cors import CORS
import zipfile
import shutil
import os
import requests
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.image_scraper import scraper, scraper_io

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello, world!"


@app.route('/picaisso/', methods=['POST', 'GET'])
def api_post():
    if request.method == 'POST':
        classes = []
        req = request.get_json()
        print(req)
        for type, query in req.items():
            if type == 'email':
                email = query
            elif type == 'url':
                url = query
            else:
                print(f"Now scraping for query {query}")
                # workflow(query)
                classes.append(query)

        res = requests.post('http://10.126.179.87:5050/inference/', json={"url": url})

        receiver_email = request.get_json()['email']
        model = zip_local_file('./model', 'model')
        dataset = zip_local_file('./downloads', 'dataset')
        return send_email(receiver_email, model, dataset, int(res.text), classes)


@app.route('/picaisso/dataset', methods=['GET'])
def upload_images():
    import shutil
    dir_name = './downloads'
    zip_path = shutil.make_archive('cats', 'zip', dir_name)
    return send_file(zip_path)


@app.route('/picaisso/model', methods=['GET'])
def upload_model():
    import shutil
    dir_name = './model'
    zip_path = shutil.make_archive('model', 'zip', dir_name)
    return send_file(zip_path)


def zip_local_file(localdir, filename):
    zip_path = shutil.make_archive(filename, 'zip', localdir)
    return zip_path


def send_email(receiver_email, filename, dataset, class_idx, classes):
    sender_email = "teampicaisso@gmail.com"
    password = "hackrice@2019"

    message = MIMEMultipart("alternative")
    message["Subject"] = "[HackRice9] Here's your dataset and model!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,

    I've built your personalized dataset and model. Thanks for using Picaisso! 

    - Team Picaisso f"""
    html = """\
    <html>
      <body>
        <p>Hi,<br><br>
           I've built your personalized dataset and model. <br>
           Download your dataset <a href="http://10.126.179.87:5000/picaisso/dataset">here.</a><br>
           Download your model <a href="http://10.126.179.87:5000/picaisso/dataset">here.</a><br>""" \
+ f'Oh, and we believe your image is a {classes[class_idx]}' + \
           """Thanks for using Picaisso!<br><br>
           - Team Picaisso
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    return "Sent email"


@app.route('/picaisso/dataset-model', methods=['GET', 'POST'])
def model_email():
    if request.method == 'POST':
        receiver_email = request.get_json()['email']
        model = zip_local_file('./model', 'model')
        dataset = zip_local_file('./downloads', 'dataset')
        return send_email(receiver_email, model, dataset)


def mock_workflow(query):
    # Query and scrape all the URLS
    gis = scraper.ImagesScraper()
    urls = gis.get_images(query, max_images=1000, fullsize=True)
    gis.cleanup()
    print(urls)


def workflow(query):
    # Query and scrape all the URLS
    gis = scraper.ImagesScraper()
    urls = gis.get_images(query, max_images=1000, fullsize=True)
    gis.cleanup()
    print(urls)

    # Send the URLs to the database
    gis_io = scraper_io.ImageScraperIO()
    gis_io.persist_images(query, urls)


if __name__ == "__main__":
    app.run(debug=True, host='10.126.179.87', port=5000)
