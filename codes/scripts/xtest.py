from pathlib import Path
path = Path(__file__).parent
rfolder = path.joinpath("rejected")
rfiles = list(filter(lambda vi: vi.suffix == ".mp4", rfolder.iterdir()))
yfolder = path.joinpath("yfiles")
yfiles = list(filter(lambda vi: vi.suffix == ".mp4", yfolder.iterdir()))
ids = []
for rn in yfiles:
    _id = rn.name.replace("[", "").replace("]", "").split(".mp4")[0][-11:]
    ids.append(_id)
for xn in rfiles:
    xid = xn.name.split(".mp4")[0][-11:]
    if xid not in ids:
        print(xn.name.replace(xid, "["+xid+"]"))
    else:
        print(xid, ids.index(xid))
