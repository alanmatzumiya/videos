from shutil import copy as cp
from pathlib import Path
path = Path.home().joinpath("Videos")
cpath = Path(__file__).parent.joinpath("downloads")
containers = list(i for i in path.joinpath("containers").iterdir() if i.is_dir())
handlers = list(i for i in path.joinpath("handler").iterdir() if i.is_dir())
data, xdata = dict(), dict()
fmts = ("jpg", "info.json", "webp", "description", "en.vtt")


for file in cpath.iterdir():
    filename = file.name
    if not filename.endswith(".mp4"):
        for x in fmts:
            filename = filename.replace(f".{x}", "")
        fileid = ""
        if filename.endswith("]"):
            fileid = filename[-12:-1]
        else:
            fileid = filename[-11:]
        if fileid not in xdata:
            xdata[fileid] = []
        xdata[fileid].append(str(file))

for c in containers:
    for file in c.joinpath("videos").iterdir():
        filename  = file.name
        if not filename.endswith(".mp4"):
            for x in fmts:
                filename = filename.replace(f".{x}", "")
            fileid = ""
            if filename.endswith("]"):
                fileid = filename[-12:-1]
            else:
                fileid = filename[-11:]
            if fileid not in data:
                data[fileid] = []
            data[fileid].append(str(file))

for h in handlers:
    for file in h.iterdir():
        filename = file.name
        if not filename.endswith(".mp4"):
            for x in fmts:
                filename = filename.replace(f".{x}", "")
            fileid = ""
            if filename.endswith("]"):
                fileid = filename[-12:-1]
            else:
                fileid = filename[-11:]
            if fileid not in data:
                data[fileid] = []
            data[fileid].append(str(file))
