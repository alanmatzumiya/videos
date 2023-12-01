# -*- coding: utf-8 -*-

from pathlib import Path
from json import load, dumps
from sys import argv
from os import system as sh
path = Path(__file__).parent
containers = list(filter(
    lambda fn: fn.is_dir() and fn.name != "__pycache__", path.iterdir()
))
jsonfile = path.joinpath("data.json")
jsonconfig = dict(indent=4, sort_keys=True, ensure_ascii=False)


def openfile():
    return load(jsonfile.open())


def savefile(json_data: dict):
    filedata = openfile()
    filedata.update(json_data)
    jsonfile.open("w").write(dumps(filedata))


if not jsonfile.is_file():
    savefile({})


def datafolder(*names):
    for folder_name in names:
        folder = path.joinpath(folder_name)
        if folder.is_dir():        
            sh(f"cd {folder} && python3 getdata.py")
        else:
            print(f"folder {folder} not found")
        
    
    
    
if __name__ == "__main__":
    params = argv[1:]
    if params:
        opt, args = params[0], params[1:]
        if opt == "get-data" and args:
            if "all" in args:
                datafolder(*[cn.name for cn in containers])
            else:
                datafolder(*args)
sh("rm -r __pycache__")

