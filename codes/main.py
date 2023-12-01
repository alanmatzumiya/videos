from pathlib import Path
from csv import DictReader as csv
from subprocess import getoutput as cli
from multiprocessing import Pool
import asyncio
path = Path(__file__).parent


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
    folder = path.joinpath("downloads")
    script = path.joinpath("download")

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


class Main:
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
            csv(path.joinpath("data/library.csv").open()),
            csv(path.joinpath("data/playlist.csv").open())
        )
        xurl = "https://music.youtube.com/watch?v="
        for x in lb:
            for k, v in x.items():
                if "URL" in k and xurl in v:
                    vid = v.replace(xurl, "")
                    self.library[vid] = x
                    if not vid in self.ids:
                        self.ids.append(vid)
                        break
        for x in pl:
            for k, v in x.items():
                if "ID" in k and len(v) == 11:
                    self.playlist[v.replace(xurl, "")] = x
                    vid = v.replace(xurl, "")
                    if not vid in self.ids:
                        self.ids.append(vid)
                        break
