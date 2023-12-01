from pathlib import Path
from csv import DictReader
url = "https://www.youtube.com"
ids = []
vids = []
xpath = Path.home().joinpath("Downloads")
library = DictReader(xpath.joinpath("library.csv").open())
playlist = DictReader(xpath.joinpath("playlist.csv").open())


for x in library:
    for k, v in x.items():
        if "url" in k.lower().split():
            v_id = v.split("watch?v=")[-1]
            v_url = f"{url}/watch?v={v_id}"
            ids.append(dict(id=v_id, url=v_url))
            vids.append(v_id)

for x in playlist:
    for k, v in x.items():
        if "id" in k.lower().split() and len(v) == 11:
            v_id = v
            v_url = f"{url}/watch?v={v_id}"
            ids.append(dict(id=v_id, url=v_url))
            vids.append(v_id)

xpath.joinpath("video-ids.txt").open("w").write(
    "\n".join(vids)
)