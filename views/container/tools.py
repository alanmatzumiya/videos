from pathlib import Path
from string import ascii_lowercase
abc = list(ascii_lowercase)


def getfilesize(filepath: Path):
    return filepath.stat().st_size * 1.0e-6


def getfiles(folder: Path, ext: str, *args):
    fmts = []
    for fmt in (ext,) + args:
        fmts.append(
            f".{fmt}" if not fmt.startswith(".") else fmt
        )
    return list(filter(
        lambda fi: fi.suffix in fmts,
        folder.iterdir()
    ))
