from src.image_scraper import scraper

if __name__ == "__main__":
    gis = scraper.GImagesScraper()
    res = gis.get_images("cats", max_images=1000)
    print(res)
