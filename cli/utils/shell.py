
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
