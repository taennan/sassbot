import shutil
from pathlib import Path

from utils import ProjectTree

def _rm_app_dist(root):
    """ """
    tree = ProjectTree(root)
    for path in tree.app_dist.iterdir():
        if path.name != "responses":
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)

def _rm_saved_models(root):
    """ """
    tree = ProjectTree(root)
    for path in tree.saved_models.iterdir():
        if path.is_dir():
            shutil.rmtree(path)

def clear(front, back, root):
    """ """
    tree = ProjectTree(root)

    if front and not back:
        _rm_app_dist(root)
    elif back and not front:
        _rm_saved_models(root)
    else:
        _rm_app_dist(root)
        _rm_saved_models(root)
