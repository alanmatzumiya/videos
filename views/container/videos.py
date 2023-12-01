# -*- coding: utf-8 -*-

from json import load, loads, dumps
from pathlib import Path
from random import sample
from os import environ, system as cmd
from time import sleep
from tools import getfiles, getfilesize, abc
environ["TERM"] = "xterm"
path = Path.home().joinpath("Videos")
container_path = path.joinpath("container")
containers_ids = abc.copy()
for n in range(1, 5):
    for i in abc:
        containers_ids.append(f"{i}{n}")


class Container:
    content, videoIds, metadata = [], [], []
    total_size, free_space, available_space = 0.0, 0.0, False

    def __init__(self, ident):
        self.id = ident
        self.giturl = f"https://github.com/circuitalmynds/music_{ident}"
        self.path = container_path.joinpath(ident)
        self.datafile = self.path.joinpath("info.json")
        self.dataset = self.path.joinpath("dataset.json")
        self.write_scripts()
        self.update_data()

    def update_data(self):
        cmd(f"python3 {self.path}/getdata.py")
        datafile = load(self.datafile.open())
        self.content, self.total_size, self.available_space = (
            datafile[key] for key in (
                "content", "total_size", "available_space"
            )
        )
        if self.available_space:
            self.free_space = 9.5e2 - self.total_size
        else:
            self.free_space = 0.0
        self.videoIds = list(map(lambda v: v["id"], self.content))
        for Id in self.videoIds:
            if not Path(self.get_video(Id)["name"].replace(
                    ".mp4", ".info.json"
            )):
                cmd(f"cd {self.path} && bash get-video {Id} --only-data")
        self.get_metadata()
        return datafile

    @property
    def info(self):
        return self.update_data()

    def get_video(self, video_id: str):
        video = list(filter(
            lambda xn: xn["id"] == video_id, self.content
        ))
        return video[0] if video else {}

    def getdata(self, video_id: str):
        meta = dict.fromkeys([
            "title", "url", "image",
            "description", "duration", "keywords"
        ], "")
        meta["id"] = video_id
        if video_id not in self.videoIds:
            return meta
        else:
            video = self.get_video(video_id)
            meta["url"] = video["url"]
            desc, datainfo, webp, jpg = (
                Path(str(video["path"]).replace(".mp4", fmt))
                for fmt in (".description", ".info.json", ".webp", ".jpg")
            )
            info = load(datainfo.open()) if datainfo.is_file() else {}
            if info.get("title"):
                meta["title"] = info["title"]
            else:
                meta["title"] = video["name"].split(video_id)[0][:-1]
            if desc.is_file():
                meta["description"] = desc.open().read()
            elif info.get("description"):
                meta["description"] = info["description"]
            if info.get("duration"):
                meta["duration"] = "{}:{}".format(*divmod(int(info["duration"]), 60))
            if info.get("tags"):
                meta["keywords"] = ", ".join(info["tags"])
            if webp.is_file():
                meta["image"] = f"{self.giturl}/raw/main/videos/{webp.name}"
            elif jpg.is_file():
                meta["image"] = f"{self.giturl}/raw/main/videos/{jpg.name}"
            return meta

    def get_metadata(self):
        self.metadata = list(self.getdata(Id) for Id in self.videoIds)
        self.dataset.open("w").write(dumps(
            self.metadata,
            indent=4,
            sort_keys=True,
            ensure_ascii=True
        ))

    def write_scripts(self):
        builtins = Path(__file__).parent.joinpath("builtins")
        main, getdata, get_video, push = (
            builtins.joinpath(f"{x}.txt").open().read()
            for x in ("main", "getdata", "get-video", "push")
        )
        getdata = getdata.replace("<REPO_ID>", self.id)
        push = push.replace("<REPO_ID>", self.id)
        self.path.joinpath("main.py").open("w").write(main)
        self.path.joinpath("getdata.py").open("w").write(getdata)
        self.path.joinpath("get-video").open("w").write(get_video)
        self.path.joinpath("push").open("w").write(push)

    def add_files(self, files):
        for fn in files:
            self.free_space -= fn["size"]
            if self.free_space > 0:
                Path(fn["path"]).rename(self.path.joinpath(f"videos/{fn['name']}"))
                sleep(1)
            else:
                sleep(10)
                self.update_data()
                break

    def update(self):
        cmd(
            f"cd {self.path} && python3 -m main update"
        )
        print(*[
            f"Id: {self.id}",
            f"total size: {self.total_size}",
            f"free space: {self.free_space}"
        ], sep="\n")


class Handler:
    path = dict({
        name: path.joinpath(name)
        for name in ("waiting", "rejected", "trash", "data")
    })
    dataformat = (".description", ".info.json", ".webp", ".jpg")

    def waiting_files(self):
        data = []
        files = getfiles(self.path["waiting"], "mp4")
        for fn in files:
            sn = getfilesize(fn)
            if round(sn) < 95.0:
                data.append(dict(
                    path=str(fn), name=fn.name, size=sn
                ))
        return data

    def rejected_files(self):
        data = []
        files = getfiles(self.path["rejected"], "mp4")
        for fn in files:
            sn = getfilesize(fn)
            if round(sn) >= 95.0:
                data.append(dict(
                    path=str(fn), name=fn.name, size=sn
                ))
        return data

    @staticmethod
    def data_sample(data, size):
        files = []
        sn = 0.0
        for fn in sample(data, len(data)):
            fs = fn["size"]
            sn += fs
            if sn < size:
                files.append(fn)
            else:
                sn -= fs
                break
        return files

    @staticmethod
    def update_containers():
        datainfo = {}
        for _id in containers_ids:
            _cont = Container(_id)
            datainfo[_id] = dict(
                content=_cont.content,
                total_size=_cont.total_size,
                available_space=_cont.available_space
            )
        return datainfo

    @staticmethod
    def get_available_containers():
        info = {}
        _info = Handler.update_containers()
        for x, y in _info.items():
            if y["available_space"]:
                info[x] = y
        return info


class DataSet:
    obj = []

    def __init__(self):
        self.obj = []

    def get_sample(self, data):

        return

    @staticmethod
    def proto():
        return dict.fromkeys([
            "description", "duration", "image", "keywords", "title", "url"
        ], "")


metafile = path.joinpath("metadata.json")
jsondata = []
for _id in containers_ids:
    cont = Container(_id)
    jsondata.extend(cont.metadata)
    cont.update()

metafile.open("w").write(dumps(
    jsondata,
    indent=4,
    sort_keys=True,
    ensure_ascii=True
))

"""
handler = Handler()
for _id in handler.get_available_containers():
    cont = Container(_id)
    yfiles = handler.data_sample(handler.waiting_files(), cont.free_space)
    cont.add_files(yfiles)
    sleep(5)
    cont.update()
    sleep(5)
"""
