from pathlib import Path
path = Path.home().joinpath("Videos")
ids = []
conts = list(filter(
    lambda x: x.is_dir(),
    path.joinpath("container").iterdir()
))
trash = list(filter(
    lambda x: x.suffix == ".mp4",
    path.joinpath("trash").iterdir()
))

for cont in conts:
    txt = cont.joinpath("videos/ids.txt")
    if txt.is_file():
        for l in txt.open().readlines():
            ids.append(l.split()[-1])

for t in trash:
    isvideo = False
    for r in ids:
        if r in t.name:
            isvideo = True
            break
    if not isvideo:
        print(str(path.joinpath(f"x/{t.name}")))