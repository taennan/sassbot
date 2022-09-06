import sys
from pathlib import Path

def add_prj_module(module_name):
    """Just a quick fix"""
    path = str((Path(__file__).parent.parent.parent) / module_name)
    if path not in sys.path:
        sys.path.append(path)
