"""
sassbot

Usage:
  sassbot build [-f] [-b] [-p <port>] [-r <root>]
  sassbot process -i <in> -o <out> [--start <start>] [--stop <stop>] [-r <root>]
  sassbot train -i <in> -o <out> [--start <start>] [--stop <stop>] [-r <root>]
  sassbot clear [-f] [-b] [-r <root>]
  sassbot run [-r <root>]
  sassbot help

Options:
  -h, --help     Show this screen
  -f, --front    Execute command in the frontend of the project
  -b, --back     Execute command in the backend of the project
  -i <in>, --in <in>      Input dirame for 'process' or 'train' commands
  -o <out>, --out <out>   Output dirame for 'process' or 'train' commands
  --start <start>   Data row to start processing or training [default: 0]
  --stop <stop>     Data row to end processing or training. Leave as negative to make infinite [default: -1]
  -p <port>, --port <port>   Local port to use when running server [default: 5000]
  -r <root>, --root <root>   Project root directory. Needed if using this script outside project root [default: ./]

"""

import sys
from pathlib import Path

from docopt import docopt

from commands import (
    build,
    train,
    process,
    clear,
    run,
)

if __name__ == "__main__":
    args = docopt(__doc__, version="0.0.1")

    front, back, in_, out, start, stop, port, root = (
        args["--front"],
        args["--back"],
        args["--in"],
        args["--out"],
        args["--start"],
        args["--stop"],
        args["--port"],
        args["--root"],
    )

    # Converts args to...
    #  Ints
    start = int(start)
    stop  = int(stop)
    port  = int(port)
    #  Full path to make this easier to work with than './'
    root = Path(root)
    if not root.root:
        root = Path.cwd() / root

    if args["build"]:
        build(front, back, port, root)
    elif args["train"]:
        train(in_, out, start, stop, root)
    elif args["process"]:
        process(in_, out, start, stop, root)
    elif args["clear"]:
        clear(front, back, root)
    elif args["run"]:
        run(root)
    elif args["help"]:
        print(__doc__, end="")
        sys.exit(0)
