import os
from pathlib import Path

from utils import ProjectTree, sh, node_pm

def _write_vite_env(path, **kwargs):
    """ """
    text = ""
    for key, value in kwargs:
        text += f"VITE_{key}={value}"

    with open(path, "w") as file:
        file.write(text)

def _build_front(port, root):
    """ """
    tree = ProjectTree(root)

    _write_vite_env(tree.front_env, PORT=port)

    os.chdir(tree.front)
    node_pm("install")
    node_pm("build", "run build")
    os.chdir(tree.root)

def _build_back(root):
    """ """
    tree = ProjectTree(root)

    # Sets up virtual environment
    sh(f"python3.9 -m venv {tree.venv}")
    sh(f"{tree.pip} install -r {tree.back_requirements}")

    # Processes data and builds model if input datasets are specified
    raise RuntimeError("UNIMPLEMENTED")

def build(front, back, port, root):
    """ """

    # sassbot build -f
    if front and not back:
        _build_front(port, root)
    # sassbot build -b
    elif back and not front:
        _build_back(root)
    # sassbot build -fb
    else:
        _build_front(port, root)
        _build_back(root)
