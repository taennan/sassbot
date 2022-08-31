"""
sassbot

Command line entry point for the sassbot project

Usage:
  sassbot build [-f | -b] [--t-data <t-data>] [--t-out <t-out>] [--p-data <p-data>] [--p-out <p-out>] [-r <root>] [-p <port>]
  sassbot process -i <in> -o <out> [--start <start>] [--stop <stop>] [-r <root>]
  sassbot train -i <in> -o <out> [-r <root>]
  sassbot clear [-f | -b] [-r <root>]
  sassbot run [-r <root>]
  sassbot help

Options:
  -h, --help     Show this screen
  -f, --front    Execute command in the frontend of the project
  -b, --back     Execute command in the backend of the project
  --t-data <t-data>  Name of file to train algorithm on. Leave as '' to ignore [default: main-data-processed.csv]
  --t-out <t-out>  Name of trained model [default: 'tf_model']
  --p-data <p-data>  Name of file to preprocess. Leave as '' to ignore [default: main-data-unprocessed.csv]
  --p-out <p-out>  Name of processed file. Leave as '' for auto naming [default: '']
  -r <root>, --root <root>  Project root directory. Needed if using this script outside project root [default: ./]
  -p <port>, --port <port>  Local port to use when building and running [default: 5000]

  -i <in>, --in <in>  Input dirame for 'process' or 'train' commands
  -o <out>, --out <out>  Output dirame for 'process' or 'train' commands
  --start <start>  Data row to start processing [default: 0]
  --stop <stop>  Data row to end processing. Leave as negative to make infinite [default: -1]

"""

import sys
import os
import shutil
import subprocess as sp
from pathlib import Path

from docopt import docopt


def sh(string, capture_output=False):
    """Runs a subprocess"""
    return sp.run(string.split(), capture_output=capture_output)

def node_pm(yarn_args="", npm_args=""):
    """Runs a command with an available Node package manager"""
    res = sh("which yarn", capture_output=True)
    if res.returncode == 0:
        args = yarn_args or npm_args
        sh(f"yarn {args}")
    else:
        args = npm_args or yarn_args
        sh(f"npm {args}")


def build(root, front, back, port, trn_data, trn_out, prc_data, prc_out):
    """ """

    def build_front():
        """ """
        front_dir = Path(root) / "front"

        env_file = front_dir / ".env"
        env_file.write_text(f"VITE_PORT={port}")

        os.chdir(front_dir)
        node_pm("install")
        node_pm("build", "run build")

        os.chdir(root)

    def build_back():
        """ """
        back_dir = Path(root) / "back"
        venv_bin = back_dir / "venv" / "bin"
        pip = venv_bin / "pip"
        py  = venv_bin / "python"
        setup_py = back_dir / "src" / "ml" / "setup.py"

        # Sets up virtual environment
        sh(f"python3.9 -m venv {back_dir}/venv")
        sh(f"{pip} install -r {back_dir}/requirements.txt")

        # Processes data and builds model if input datasets are specified
        if prc_data:
            sh(f"{py} {setup_py} process -d {prc_data} -o {prc_out}")
        if trn_data:
            sh(f"{py} {setup_py} model -d {trn_data} -o {trn_out}")

        os.chdir(root)

    if front and not back:
        build_front()
    elif back and not front:
        build_back()
    else:
        build_front()
        build_back()

def clear(root, front, back):
    """ """
    src_dir = Path(root) / "back" / "src"
    app_dist  = src_dir / "static"
    model_dir = src_dir / "tf_model"

    def rm_app_dist():
        """ """
        for path in app_dist.iterdir():
            if path.name != "responses":
                if path.is_file():
                    path.unlink()
                else:
                    shutil.rmtree(path)

    if front and not back:
        rm_app_dist()
    elif back and not front:
        shutil.rmtree(model_dir)
    else:
        rm_app_dist()
        shutil.rmtree(model_dir)

def run(root):
    """ """
    back_dir = Path(root) / "back"
    venv_bin = back_dir / "venv" / "bin"
    py = venv_bin / "python"
    front_dir = Path(root) / "front"
    env_file  = front_dir / ".env"

    # Gets port specified at build step from .env
    port_arg = ""
    env_vars = env_file.read_text().split("\n")
    for e in env_vars:
        if "VITE_PORT" in e:
            port = e.split("=")[1]
            port_arg = f"--port {port}"
            break

    #os.chdir(back_dir)
    sh(f"{py} -m flask run {port_arg}")

    os.chdir(root)


if __name__ == "__main__":
    args = docopt(__doc__, version="0.0.1")

    r, f, b, p, td, to, pd, po = (
        args["--root"],
        args["--front"],
        args["--back"],
        args["--port"],
        args["--t-data"],
        args["--t-out"],
        args["--p-data"],
        args["--p-out"],
    )

    # Converts to full path to make this easier to work with than './'
    r = Path.cwd() if r in [".", "./"] else r

    if args["build"]:
        build(r, f, b, p, td, to, pd, po)
    elif args["process"]:
        print("Unimplemented")
        sys.exit(0)
    elif args["train"]:
        print("Unimplemented")
        sys.exit(0)
    elif args["clear"]:
        clear(r, f, b)
    elif args["run"]:
        run(r)
    elif args["help"]:
        print(__doc__, end="")
        sys.exit(0)
