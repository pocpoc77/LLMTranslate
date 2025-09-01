from pathlib import Path

def filenameFromPath(path):
    name = path.replace(Path(path).suffix, "")
    return name
