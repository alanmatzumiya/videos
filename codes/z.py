from requests import get
from bs4 import BeautifulSoup


def gitdata(repo):
    content = []
    giturl = f"https://github.com/circuitalmynds/{repo}"
    url = f"{giturl}/blob/main/videos"
    links = BeautifulSoup(
        get(url).text, "html.parser"
    ).find("body").findAll("a")
    for link in links:
        href = link.get("href")
        if href.endswith(f".mp4"):
            content.append(dict(
                filename=link.get("title"),
                url=f"{url}{href}?raw=true"
            ))
    return content
print(get(f"https://github.com/circuitalmynds/music_a/blob/main/videos").content)