# -*- coding: utf-8 -*-

from os import system as sh
from multiprocessing import Pool
from string import ascii_lowercase
giturl = "https://github.com/circuitalmynds"
containers = list(ascii_lowercase)
procs = []


def clone(cont_id):
    sh(
        f"git clone {giturl}/music_{cont_id}1.git {cont_id}1"
    )


x = containers[:6]
y = containers[6:12]
z = containers[12:18]
w = containers[18:24]
h = containers[24:]

for v in [x, y, z, w, h]:
    procs.extend(v)
    with Pool(len(procs)) as p:
        p.map(clone, procs)
    procs.clear()
