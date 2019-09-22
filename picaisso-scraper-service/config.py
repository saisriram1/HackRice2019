import os
from pathlib import Path


class Config:
    ROOT = Path(__file__).parent
    CHROMEDRIVER_PATH = ROOT.joinpath('./vendor/chromedriver.exe').as_posix()
    DOWNLOAD_DIR = ROOT.joinpath('./downloads')
    DB_PARAMS = {"host": "35.193.255.40", "database": "hackrice9", "user": "shryans", "password": "shryans"}
