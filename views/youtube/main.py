# -*- coding: utf-8 -*-

from multiprocessing import Pool
from subprocess import getoutput as cli
from utils import yt_path, opencsv, Path
import asyncio
root = Path(__file__).parent.parent


def runcmd(**kwargs):
    src = kwargs.get("script")
    cmd = kwargs.get("command")
    if src:
        args = " ".join(kwargs.get("args"))
        filepath = Path(str(src))
        out = cli(f"cd {filepath.parent} && bash {filepath.name} {args}")
        print(out)
        return out
    elif cmd:
        out = cli(cmd)
        print(out)
        return out


def proc(arg: dict):
    runcmd(**arg)


class Download:
    folder = yt_path.joinpath("downloads")
    script = root.joinpath("bash/video-download")

    def __init__(self, *args):
        self.task = args

    def get(self, *ids):
        fdata = [{"script": self.script, "args": ("video_id", t)} for t in ids]
        with Pool(len(fdata)) as procs:
            procs.map(proc, fdata)

    def run(self):

        async def init():
            self.get(*self.task)
            await asyncio.sleep(3)

        async def processes():
            await asyncio.gather(init())
            return
        asyncio.run(processes())


class Task:
    ids, library, playlist = [], {}, {}

    def __init__(self):
        self.update()
        n = len(self.ids) // 5
        for i in range(n):
            ids = self.ids[i*5:i*5+5]
            for j in ids:
                print(self.library.get(j) or self.playlist.get(j))
            Download(*self.ids[i*5:i*5+5]).run()

    def update(self):
        lb, pl = (
            opencsv(yt_path.joinpath("data/library.csv")),
            opencsv(yt_path.joinpath("data/playlist.csv"))
        )
        xurl = "https://music.youtube.com/watch?v="
        for x in lb:
            for k, v in x.items():
                if "URL" in k and xurl in v:
                    vid = v.replace(xurl, "")
                    self.library[vid] = x
                    if vid not in self.ids:
                        self.ids.append(vid)
                        break
        for x in pl:
            for k, v in x.items():
                if "ID" in k and len(v) == 11:
                    self.playlist[v.replace(xurl, "")] = x
                    vid = v.replace(xurl, "")
                    if vid not in self.ids:
                        self.ids.append(vid)
                        break


class YouTube:
    url = "https://www.youtube.com"
    data = dict(
        path=yt_path.joinpath("data"),
        library=[], playlist=[]
    )

    def __init__(self):
        self.update_data()

    def get_ids(self, name):
        return list(map(
            lambda x: x["id"], self.data.get(name)
        ))

    def get_urls(self, name):
        return list(map(
            lambda x: x["url"], self.data.get(name)
        ))

    def update_data(self):
        self.data["library"] = self.library_data()
        self.data["playlist"] = self.playlist_data()

    def library_data(self):
        file, data = opencsv(self.data["path"].joinpath("library.csv")), []
        for x in file:
            for k, v in x.items():
                if "url" in k.lower().split():
                    v_id = v.split("watch?v=")[-1]
                    v_url = f"{self.url}/watch?v={v_id}"
                    data.append(dict(id=v_id, url=v_url))
        return data

    def playlist_data(self):
        file, data = opencsv(self.data["path"].joinpath("playlist.csv")), []
        for x in file:
            for k, v in x.items():
                if "id" in k.lower().split() and len(v) == 11:
                    v_id = v
                    v_url = f"{self.url}/watch?v={v_id}"
                    data.append(dict(id=v_id, url=v_url))
        return data

