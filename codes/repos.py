# -*- coding: utf-8 -*-

from pathlib import Path
from string import ascii_lowercase
path = Path(__file__).parent
abc = list(ascii_lowercase)
containers = abc.copy()
for i in (1, 2, 3, 4):
    for j in abc:
        repo = path.joinpath(j + str(i))
        if not repo.is_dir():
            print(str(repo))

