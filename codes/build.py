# -*- coding: utf-8 -*-

from pathlib import Path
from libs.request import Http
from libs.shell import CLI
from libs.utils import getjson
from csv import DictReader
path = Path(__file__).parent


class Data:
    ids, playlist, library = [], [], []

    def __init__(self):
        self.update()

    def update(self):
        ids = []
        self.playlist.clear()
        self.library.clear()
        for x in DictReader(path.joinpath("data/playlist.csv").open()):
            x_id = x.get("Playlist Id")
            if len(x_id) == 11:
                self.playlist.append(x)
                self.ids.append(x_id)
        for x in DictReader(path.joinpath("data/library.csv").open()):
            self.library.append(x)
            self.ids.append(x.get("Song URL").replace(
                "https://music.youtube.com/watch?v=", ""
            ))
        self.ids = list(dict.fromkeys(ids, None))


class Downloads:
    path = path.joinpath("downloads")
    files = dict()

    def __init__(self):
        self.update()

    def update(self):
        for file in self.path.iterdir():
            filename = file.name
            if filename.endswith(".mp4"):
                fileid = file.name.split(".mp4")[0][-11:]
                self.files[fileid] = filename

    def getdata(self, data_id):
        if data_id in self.files:
            datafile = dict()
            filename = self.files[data_id]
            filepath = str(self.path.joinpath(filename))
            info = getjson(Path(filepath.replace(".mp4", ".info.json")))
            for key in (
                "id", "title", "duration", "filesize",
                "webpage_url", "categories", "tags", "thumbnail"
            ):
                datafile[key] = info[key]
            datafile.update(dict(
                filepath=filepath, filename=filename,
                description=Path(filepath.replace(".mp4", ".description")).open().read(),
                image=filepath.replace(".mp4", ".jpg"),
            ))
            return datafile

        else:
            return dict()

    @staticmethod
    def get(**data):
        keys = ("video_title", "video_id", "playlist_id")
        for i in keys:
            if i in data:
                CLI.input(
                    f"bash download '{i}' '{data.get(i)}'"
                )


class YouTube:
    url = "https://www.youtube.com"
    data, downloads = Data(), Downloads()

    def search(self, v_title):
        return Http(self.url).html_parser("results", **dict(search_query=v_title))

    def watch(self, v_id):
        return Http(self.url).html_parser("watch", **dict(v=v_id))

    def get_ids(self, v_title):
        data = {v_title: []}
        try:
            for q in self.search(v_title).find('body').prettify().split('"videoId":"'):
                r = q.split('"')[0]
                if len(r) == 11 and r not in data[v_title]:
                    data[v_title].append(r)
        except UnicodeEncodeError:
            pass
        return data

    def get_metadata(self, v_id):
        keys = ("name", "property", "itemprop")
        metadata = {key: [] for key in keys}
        data = self.watch(v_id).find('head').find_all('meta')
        for x in data:
            for y in metadata:
                if x.get(y):
                    metadata[y].append(x.attrs)
        return metadata

    def is_id(self, **data):
        v_html, v_id = data.get("html"), data.get("video_id")
        if v_id:
            v_html = self.watch(v_id)
        if Http.is_html(v_html):
            try:
                return '"status":"ERROR"' not in v_html.find("body").find("script").string
            except UnicodeEncodeError:
                return False
        else:
            return False
