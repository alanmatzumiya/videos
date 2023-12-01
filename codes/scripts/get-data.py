# -*- coding: utf-8 -*-

from pathlib import Path
from json import load, dumps, JSONDecodeError
from sys import argv
from os import system
path = Path(__file__).parent
datafile = path.joinpath("data.json")
folders = {
    fn.name: fn for fn in path.iterdir()
    if fn.is_dir() and fn.name != "__pycache__"
}
dataconf = dict(indent=4, sort_keys=True, ensure_ascii=False)


def savefile(key, value):
    xdata, ydata = {}, {key: value}
    try:
        xdata = load(datafile.open())
    except JSONDecodeError:
        datafile.open("w").write(dumps(xdata, **dataconf))
    xdata.update(ydata)
    datafile.open("w").write(dumps(xdata, **dataconf))


def getdata(name):
    folder = folders.get(name)
    if folder:
        fdata = []
        for xn in folder.iterdir():
            if xn.is_file() and xn.name.endswith(".mp4"):
                fdata.append(xn.name)
        savefile(name, fdata)


def datacompare():
    sample_file = path.joinpath("sample.json")
    data, sample = load(datafile.open()), {}
    if sample_file.is_file():
        sample = load(sample_file.open())      
    for k in data.keys():
        files = sample.get(k)        
        if files:
            datafiles = data[k]      
            for ki in data[k]:                
                if ki not in files:
                    print(f"file {ki} not found in folder {k}")
        elif type(files) != list:
            print(f"folder {k} not found")


if __name__ == "__main__":
    args = argv[1:]
    if args:
        if "all" in args:
            for n in folders:
                getdata(n)
        elif "compare" in args:
            datacompare()
        else:
            for arg in args:
                getdata(arg)
    system("rm -r __pycache__")

