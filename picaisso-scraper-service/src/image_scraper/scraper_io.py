import os

import mysql.connector
from mysql.connector import errorcode
from timeit import default_timer as timer
import requests

from config import Config
import src.image_scraper.processor as processor


class ImageScraperIO(object):
    def __init__(self):
        self.conn, self.cur = self.__class__._attempt_connect_to_db()

    def persist_images(self, query, urls):
        """ Save images to an external database."""
        func_start_time = timer()
        print('Persisting found images')
        num_urls = 0

        # Send the URLs one by one

        for index, url in enumerate(urls):
            if not url:
                continue
            try:
                # Save image to disk
                processor.save_image(url, Config.DOWNLOAD_DIR)
                # Send URL to database
                tbl_name = self.__class__._sanitize_table_name(query)
                self._send_to_db(tbl_name, url)
                num_urls += 1
            except:
                print('err on: ', url)

        # Clean up after we're done with all open connections
        self._cleanup()
        print('Number of links: {}'.format(num_urls))
        print('Done in {:.2f}s'.format(timer() - func_start_time))

    @staticmethod
    def _sanitize_table_name(name):
        """Sanitizes the table name to prevent SQL injection attack.
        NOTE: If we were actually writing for production, we'd go about solving this in a much more secure way.
        But since we're pressed for time in this hackathon, we're solving it with this hack for now.
        """
        return "".join(name.split())

    @staticmethod
    def _attempt_connect_to_db():
        """Attempts to connect to the external MySQL database."""
        try:
            conn = mysql.connector.connect(**Config.DB_PARAMS)
            assert conn.is_connected()
            print("Connected here")
            db_info = conn.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            return conn, conn.cursor()
        except AssertionError:
            print("Failed to connect to DB")

    def _create_update_table(self, sanitized_name):
        CREATE_TABLE_QUERY = f"CREATE TABLE {sanitized_name} (id INT AUTO_INCREMENT PRIMARY KEY, url TEXT)"
        print("Creating table {}: ".format(sanitized_name), end='')
        self.cur.execute(CREATE_TABLE_QUERY)

    def _send_to_db(self, tbl_name, url):
        """Sends the image URL to the external database"""
        sanitized_name = self.__class__._sanitize_table_name(tbl_name)

        self.cur.execute(f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=\'{sanitized_name}\'")
        table_exists = self.cur.fetchall()

        if not table_exists:
            self._create_update_table(sanitized_name)
        else:
            UPDATE_TABLE_QUERY = f"INSERT INTO {sanitized_name} VALUES (NULL, \'{url}\')"
            self.cur.execute(UPDATE_TABLE_QUERY)
            print(f"Wrote URL to {tbl_name}")

        # try:
        #     self._create_update_table(sanitized_name)
        # except:
        #     # except mysql.connector.Error as err:
        #     # if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        #     UPDATE_TABLE_QUERY = f"INSERT INTO f{sanitized_name} VALUES (NULL, \'{url}\', \'{img_binary}\')"
        #     self.cur.execute(UPDATE_TABLE_QUERY)
        #     print(f"Wrote URL and binary to {tbl_name}")
        #     # else:
        #     #     print(err.msg)
        # else:
        #     print("OK")

    def _cleanup(self):
        """Closes and cleans up the DB connection"""
        self.cur.close()
        self.conn.close()
        print("MySQL connection is closed")
