import random as rand

from utils import STATIC_DIR

RESP_DIR = STATIC_DIR / "responses"

def responses(polite: bool) -> str:
    """ """
    file_name = "polite" if polite else "impolite"
    path = RESP_DIR / file_name
    return path.read_text()

def all_responses() -> str:
    """ """
    return responses(True) + responses(False)

def random_response(polite: bool) -> str:
    """Returns a polite or impolite greeting as specified in args"""
    resp = responses(polite).split("\n")
    # Removes empty string at the end if the file ends with a '\n'
    if resp[-1] == "":
        resp.pop(-1)
    return rand.choice(resp)
