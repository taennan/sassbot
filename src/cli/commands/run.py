from pathlib import Path

from utils import ProjectTree, sh

def _read_env_file(file_path) -> dict:
    """ """
    res = {}
    lines = env_file.read_text().split("\n")
    for var in lines:
        key, val = var.split("=")[:2]
        res[key] = val
    return res

def run(root):
    """ """
    tree = ProjectTree(root)

    port_var = _read_env_file(tree.front_env).get("VITE_PORT")
    port_arg = f"--port {port_var}" if port_var is not None else ""

    sh(f"{tree.python} -m flask run {port_arg}")
