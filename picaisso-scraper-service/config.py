import os
from pathlib import Path


class Config:
    ROOT = Path(__file__).parent
    CHROMEDRIVER_PATH = ROOT.joinpath('./vendor/chromedriver.exe').as_posix()
    DB_PARAMS = {"host": "35.193.255.40", "database": "mydb", "user": "shryans", "password": "shryans"}