import os
from pathlib import Path


class Config:
    ROOT = Path(__file__).parent
    CHROMEDRIVER_PATH = ROOT.joinpath('./vendor/chromedriver.exe').as_posix()
