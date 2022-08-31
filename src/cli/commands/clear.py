import shutil
from pathlib import Path

from utils import ProjectTree

def _rm_app_dist(dist_dir):
    """ """
    for path in Path(dist_dir).iterdir():
        if path.name != "responses":
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)

def _rm_saved_models(model_dir):
    """ """
    for path in Path(model_dir).iterdir():
        shutil.rmtree(path)

def clear(front, back, root):
    """ """
    tree = ProjectTree(root)

    if front and not back:
        _rm_app_dist(tree.app_dist)
    elif back and not front:
        _rm_saved_models(tree.models)
    else:
        _rm_app_dist(tree.app_dist)
        _rm_saved_models(tree.models)
