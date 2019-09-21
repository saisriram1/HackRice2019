import mysql.connector

from config import Config
from src.image_scraper import scraper, processor

if __name__ == "__main__":
    gis = scraper.GImagesScraper()
    urls = gis.get_images("chinese yuan bills", max_images=1000, fullsize=False)
    gis.cleanup()

    # conn = mysql.connector.connect()
    # processor.persist_images(conn, urls)
    print(urls)
