import sys
from pathlib import Path

import stringth

from utils import ProjectTree, add_prj_module
add_prj_module("ml")
from layers import ProcessText
from data import DATA_DIR, RAW_DATA_DIR, DATA_COLS


def _convert_raw_csv_stem(full_path):
    """ """
    sffx = ""
    for s in full_path.suffixes:
        sffx += s
    stem = Path(full_path).stem
    stem = stem.removesuffix("-unprocessed")
    return full_path.parent / f"{stem}-processed{sffx}"

def convert_csv_name(path):
    """ """
    path = Path(path)
    sffx = stringth.join(*path.suffixes)
    stem = path.stem.removesuffix("-unprocessed")
    return f"{stem}-processed{sffx}"

def process_df_text(df):
    """ """
    text = ProcessText()(df.text.values).numpy()
    text = df.text.apply(lambda i: i.decode())
    return text

def save_df(df, name, root):
    """ """
    tree = ProjectTree(root)
    df.to_csv(tree.processed_data / name,  header=False, index=False)

def _process_data(in_, out, start, stop, root):
    """
    Processes specified dataset and writes to specified output file

    Parameters 'in_' and 'out' are meant to be the names file, not the full path
    """

    print(f"Processing dataset {in_}...")

    tree = ProjectTree(root)

    df = pd.read_csv(root.unprocessed_data / in_, names=DATA_COLS)

    # Drops any columns not named 'text' or 'sentiment'
    df = df.drop(columns=[c for c in df.columns if c not in DATA_COLS])
    df = df.drop_duplicates(subset="text")
    # Gets 'start' to 'stop' rows of df
    stop = len(df) if stop < 0 else stop
    df = df[start:stop]

    df.text = process_df_text(df)

    save_name = out or convert_csv_name(in_)
    save_df(df, save_name, root)

    print(f"Saved processed dataset to {save_name}")

def process(in_, out, start, stop, root):
    """ """
    print(in_, out, start, stop, root)
    #_process_data(in_, out, start, stop, root)
