import os


def fromAssets(path: str):
    return os.path.join(os.getcwd(), "assets", path)
