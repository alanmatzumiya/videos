from pathlib import Path
xpath = Path.home().joinpath("Videos")
trash = xpath.joinpath("trash")
cts = list(filter(
    lambda cn: cn.is_dir(),
    xpath.joinpath("container").iterdir()
))
ids = []
for ci in cts:
    for li in ci.joinpath("videos/ids.txt").open().readlines():
        ids.append(li.strip().split()[-1])
wfiles = list(filter(
    lambda xi: xi.suffix == ".mp4", xpath.joinpath("trash").iterdir()
))
for wi in wfiles:
    wid = wi.name.replace("[", "").replace("]", "").split(".mp4")[0][-11:]
    if wid not in ids:
        wi.rename(str(xpath.joinpath(f"waiting/{wi.name}")))

"""
    vn = ci.joinpath("videos/ids.txt")
    # fn = ci.joinpath("videos").iterdir()
    ids = list(map(
        lambda xn: xn.strip().split()[-1],
        vn.open().readlines()
    ))
    videos = list(filter(
        lambda j: j.suffix == ".mp4",
        ci.joinpath("videos").iterdir()
    ))
    _ids = []
    for _id in ids:
        isvideo = False
        for vi in videos:
            if _id in vi.name:
                isvideo = True
                break
        if isvideo:
            _ids.append(_id)
        else:
            for vi in ci.joinpath("videos").iterdir():
                if _id in vi.name:
                    vi.rename(str(trash.joinpath(vi.name)))
    ci.joinpath("videos/ids.txt").open("w").write(
        "\n".join([f"youtube {t}" for t in _ids])
    )



    if ignore.is_file():
        lines = list(map(
            lambda li: li.strip(),
            ignore.open().readlines()
        ))
        for line in lines:
            if line != "__pycache__":
                fn = ci.joinpath(line.replace("./", ""))
                info = Path(str(fn).replace(".mp4", ".info.json"))
                desc = Path(str(fn).replace(".mp4", ".description"))
                img1 = Path(str(fn).replace(".mp4", ".webp"))
                img2 = Path(str(fn).replace(".mp4", ".jpg"))
                if fn.is_file():
                    fn.rename(str(trash.joinpath(fn.name)))
                if info.is_file():
                    info.rename(str(trash.joinpath(info.name)))
                if desc.is_file():
                    desc.rename(str(trash.joinpath(desc.name)))
                if img1.is_file():
                    img1.rename(str(trash.joinpath(img1.name)))
                if img2.is_file():
                    img2.rename(str(trash.joinpath(img2.name)))


ids = []
vids = [
    s.strip() for s in Path.home().joinpath(
        "Downloads/video-ids.txt"
    ).open().readlines()
]
for cont in conts:
    txt = cont.joinpath("videos/ids.txt")
    if txt.is_file():
        for l in txt.open().readlines():
            ids.append(l.strip().split()[-1])
    else:
        print(str(cont))

for xn in xpath.joinpath("waiting").iterdir():
    if xn.suffix == ".mp4":
        xname = str(xn)
        for i in ids:
            if i in xname:
                print(i)

print(len(ids))
print(len(vids))
for xn in xpath.joinpath("waiting").iterdir():
    if xn.suffix == ".mp4":
        xname = str(xn)
        for i in vids:
            if i in xname:
                vids.remove(i)
print(len(vids))

for i in vids:
    if i in ids:
        vids.remove(i)
print(len(vids))

for xn in xpath.joinpath("rejected").iterdir():
    if xn.suffix == ".mp4":
        xname = str(xn)
        for i in vids:
            if i in xname:
                vids.remove(i)
print(len(vids))

"""
