# -*- coding: utf-8 -*-

from os import environ
from pathlib import Path
from dotenv import load_dotenv
from subprocess import getoutput as gout
from json import load,  dumps, JSONDecodeError
root = Path(__file__).parent
load_dotenv(root.joinpath(".env"))
environ["TERM"] = "xterm"
environ["root"] = str(root)
sh = root.joinpath("bash")
videos_path = Path.home().joinpath("Videos")
videos_data = {
    x: videos_path.joinpath("data", x)
    for x in (
        "info", "description", "image", "caption"
    )
}
videos_folder = {
    x: videos_path.joinpath(x)
    for x in (
        "waiting", "rejected", "trash"
    )
}
jsonconfig = dict(
    indent=4,
    sort_keys=True,
    ensure_ascii=False
)


def install_app():
    return gout(
        f"bash {sh.joinpath('install')} app"
    )


def getdata(fileid):
    files = videos_data.get("info")
    datainfo = {}
    for x in files.iterdir():
        if fileid in x.name:
            try:
                fdata = load(x.open())
                datainfo["description"] = ""
                for key in ("id", "categories", "tags", "thumbnail", "title", "duration"):
                    datainfo[key] = fdata.get(key)
                for y in videos_data.get("description").iterdir():
                    if fileid in y.name:
                        datainfo["description"] = y.open().read()
                        break
            except JSONDecodeError:
                pass
            break
    return datainfo


def get_waiting_files():
    dpath = videos_folder.get("waiting")
    data = {}
    for fn in dpath.iterdir():
        if fn.suffix == ".mp4":
            fileid = fn.name.split("].mp4")[0][-11:]
            size = fn.stat().st_size * 1.0e-6
            data[fileid] = dict(
                filename=fn.name, filesize=size, **getdata(fileid)
            )
    dpath.joinpath("data.json").open("w").write(dumps(data, **jsonconfig))
    return data


def get_rejected_files():
    dpath = videos_folder.get("rejected")
    data = {}
    for fn in dpath.iterdir():
        if fn.suffix == ".mp4":
            fileid = fn.name.split("].mp4")[0][-11:]
            size = fn.stat().st_size * 1.0e-6
            data[fileid] = dict(
                filename=fn.name, filesize=size, **getdata(fileid)
            )
    dpath.joinpath("data.json").open("w").write(dumps(data, **jsonconfig))
    return data


def get_videos(folder_name):
    folder_path = videos_folder.get(folder_name)
    files = []
    for fn in folder_path.iterdir():
        fx, fileid = fn.name, ""
        if not fx.endswith("].mp4"):
            fileid = fx.split(".mp4")[0][-11:]
            fx = fx.split(fileid)[0]
            if fx.endswith("-"):
                fx = fx[:-1]
            fx += f" [{fileid}].mp4"
            fy = folder_path.joinpath(fx)
            if fy.is_file():
                nsize, ysize = fn.stat().st_size * 1.0e-6, fy.stat().st_size * 1.0e-6
                if nsize > ysize:
                    #fy.rename(videos_folder.get("trash").joinpath(fy.name))
                    print("1.1")
                else:
                    #fn.rename(videos_folder.get("trash").joinpath(fn.name))
                    print("1.2")
            else:
                #fn.rename(folder_path.joinpath(fx))
                print(2)

