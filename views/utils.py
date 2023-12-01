# -*- coding: utf-8 -*-

from time import ctime
from pathlib import Path
from subprocess import getoutput as gout
path = Path(__file__).parent.parent
host = gout("hostname - I").split()[-1]
port = 5000
url = f"http://{host}:{port}"


def getdate():
    dt = ctime()
    date = list(filter(lambda e: e != "", dt.split()))
    t = date[3].split(":")
    today = dict(
        day=int(date[2]), month=date[1], year=int(date[4]),
        hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2])
    )
    for i in ("hours", "minutes", "seconds"):
        s = str(today[i])
        if len(s) == 1:
            today[i] = f"0{s}"
    return "{day}-{month}-{year}, {hours}:{minutes}:{seconds}".format(**today)
