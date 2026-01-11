import os


def fromInternal(path: str):
    return os.path.join(os.getcwd(), "_internal", path)
