# -*- coding: utf-8 -*-

from pathlib import Path
from csv import DictReader
yt_path = Path(__file__).parent


def opencsv(filepath):
    return DictReader(Path(filepath).open())

