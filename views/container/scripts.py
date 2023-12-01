# -*- coding: utf-8 -*-

from pathlib import Path


def write_code(repo_id):
    repo_folder = Path.home().joinpath(f"Videos/container/{repo_id}")
    info_script = """# -*- coding: utf-8 -*-
    
from pathlib import Path
from json import load, dumps
jsonconfig = dict(
    indent=4, sort_keys=True, ensure_ascii=True
)
path = Path(__file__).parent
giturl = "https://github.com/circuitalmynds/music_<repo_id>"
videos = path.joinpath("videos")
info = path.joinpath("info.json")


def getinfo():
    return load(info.open())


def save_info(data):
    info.open("w").write(dumps(
        data, **jsonconfig
    ))


def getfiles():
    urlfile, totalsize, content = f"{giturl}/raw/main/videos", 0.0, []
    files = list(
        fi for fi in videos.iterdir() 
        if fi.suffix == ".mp4"
    )
    for file in files:
        filename = file.name
        fileid = filename.split(".mp4")[0].replace("[", "").replace("]", "")[-11:]
        size = file.stat().st_size * 1.0e-6
        content.append(dict(
            name=filename,
            id=fileid,
            size=size,
            path=str(file),
            url=f"{urlfile}/{filename}"
        ))
        totalsize += size
    return dict(
        content=content,
        total_size=totalsize,
        available_space=totalsize < 9.5e2
    )


if __name__ == "__main__":
    save_info(getfiles())
    print(getinfo())
""".replace("<repo_id>", repo_id)
    push_script = f"""#!/bin/bash
    
allow_push=$( python3 -m main get allow-push )
git_user=alanmatzumiya
username=circuitalmynds
repo=music_{repo_id}

echo *__pycache__ > .gitignore
find ./videos* -size +95M | cat >> .gitignore
if $allow_push; then

    python3 -m getdata
    python3 -m main set allow-push false

    git add .
    git commit -m "autocommit"
    git push https://$git_user:"$( head "$HOME"/secret )"@github.com/$username/$repo.git

fi"""
    for x, y in [("push", push_script), ("getdata.py", info_script)]:
        repo_folder.joinpath(x).open("w").write(y)
