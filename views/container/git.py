# -*- coding: utf-8 -*-

from requests import get
from string import ascii_lowercase
from pathlib import Path
from json import load
cont_path = Path.home().joinpath("Videos/container")
abc = list(ascii_lowercase)


class Git:
    url = "https://github.com/circuitalmynds"
    files = []

    def __init__(self, repo_id):
        self.repo_id = repo_id
        self.repo_name = f"music_{repo_id}"

    def getfiles(self):
        url = f"{self.url}/{self.repo_name}/tree/main/videos"
        fmts = (
            ".jpg", ".webp", ".description", "info.json", ".mp4"
        )
        data = get(url).json()["payload"]["tree"]["items"]
        for x in data:
            name, datatype = x["name"], x["contentType"]
            if datatype == "file" and name.endswith(fmts):
                self.files.append(dict(
                    name=x["name"],
                    path=x["path"]
                ))
        return self.files


