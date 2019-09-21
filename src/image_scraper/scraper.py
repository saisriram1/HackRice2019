import time
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from timeit import default_timer as timer

from config import Config


class GImagesScraper(object):
    """ Scrape Google images"""

    def __init__(self):
        self.browser = self.__class__._get_browser()

    def cleanup(self):
        self.browser.quit()

    @staticmethod
    def _create_storage_dir(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    @staticmethod
    def _get_browser():
        """ Create a ChromeDriver-based Selenium browser. """
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=Config.CHROMEDRIVER_PATH, options=options)
        return driver

    @staticmethod
    def _scroll_to_bottom(browser):
        """ A helper to scroll the the bottom of the page. """
        # print('Scrolling to bottom', end='')
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        loading_img = browser.find_element_by_id('isr_cld')
        while loading_img.is_displayed():
            time.sleep(0.1)

    def _find_images_on_page(self):
        """ Keep scrolling down on the page until we get the desired
            number of images, or until no new images are loading.
        """
        browser = self.browser
        max_images = self.max_images
        images = []
        images_on_page = 0
        prev_images_on_page = 0
        print('Images on page ', end='')
        while images_on_page < max_images:
            self.__class__._scroll_to_bottom(browser)
            images = browser.find_elements_by_css_selector("img.rg_ic")
            images_on_page = len(images)
            print('{} '.format(images_on_page), end=' ')
            # Did we load new images
            if images_on_page <= prev_images_on_page:
                print(" No new images")
                break
            prev_images_on_page = images_on_page

            # Click the fetch more button if present
            # Note: currently the button is always present but hidden. Still,
            # clicking it doesn't hurt.
            selector = ".ksb[value='Show more results']"
            fetch_more_button = browser.find_element_by_css_selector(selector)

            if fetch_more_button:
                browser.execute_script(
                    f"document.querySelector(\".ksb[value=\'Show more results\']\").click();")
                # '.ksb._kvc'
        return images

    def get_images(self, query, max_images=1000,
                   photos_only=True, fullsize=False):
        """ Get images from Google Image search for a given query.
            Adapted from
            https://gist.github.com/kekeblom/204a609ee295c81c3cc202ecbe68752c
        Args:
            query (str): The query to get images for.
            max_images (int): How many images to retrieve.
            photos_only (bool): Adds a flag to Google Images to display photo
                results only.
            fullsize (bool): Whether to get the original fullsize images,
                or the thumbnails only.
        Returns:
            images: List of single images. Each image can be an URL or a
                base64 encoded image.
        Raises:
            IOError: When the google images page can not be retrieved.
        """
        start_time = timer()
        self.max_images = max_images

        # Google Images URL with the query
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
        if photos_only:
            search_url += '&tbs=itp:photo'
        search_url = search_url.format(q=query)

        # Get the page contents
        self.browser.set_window_size(1436, 1022)
        self.browser.get(search_url)
        # retrieve images
        images = self._find_images_on_page()

        # Store the retrieved images
        # Image data can either bet base64 encoded images or URLs
        image_urls = set()
        if fullsize:
            # Find all links to the original images
            metas = self.browser.find_elements_by_css_selector("div.rg_meta")
            for meta in metas:
                meta_text = meta.get_attribute('textContent')
                image_urls.add(json.loads(meta_text)["ou"])
                # file_type = json.loads(meta_text)["ity"]
        else:
            # Thumbnails
            for img in images:
                image_urls.add(img.get_attribute('src'))

        # Print some stats
        time_elapsed = timer() - start_time
        print('Got {} images for query "{}" in {} seconds'.format(
            len(image_urls), query, time_elapsed))

        return list(image_urls)
