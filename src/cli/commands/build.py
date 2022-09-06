import os
from pathlib import Path

from .train import train
from .process import save_df, convert_csv_name, process_df_text
from utils import ProjectTree, sh, node_pm, add_prj_module
add_prj_module("ml")
from layers import ProcessText
from data import DATA_DIR, RAW_DATA_DIR, DATA_COLS


def _write_vite_env(root, **kwargs):
    """ """
    tree = ProjectTree(root)
    text = ""
    for key, value in kwargs:
        text += f"VITE_{key}={value}"

    with open(tree.front_env, "w") as file:
        file.write(text)

def _process_twitter_data(in_, out, root):
    """Processes the large twitter dataset from scratch"""

    print(f"Processing dataset {dataset}...")

    tree = ProjectTree(root)

    encoding = "ISO-8859-1"
    cols = ["sentiment", "id", "date", "flag", "user", "text"]

    df = pd.read_csv(tree.unprocessed_data / in_, names=cols)

    # Drops any columns not named 'text' or 'sentiment'
    df = df.drop(columns=[c for c in df.columns if c not in DATA_COLS])
    df = df.reindex(columns=DATA_COLS)
    df = df.drop_duplicates(subset="text")
    # Sets values of positive rows to 1 since they're listed as 4 for some reason
    df.sentiment = df.sentiment.replace(4,1)

    df.text = process_df_text(df)

    save_df(df, out, tree.root)

    print(f"Saved processed dataset to {save_path}")

def _build_front(port, root):
    """ """
    tree = ProjectTree(root)

    _write_vite_env(tree.root, PORT=port)

    os.chdir(tree.front)
    node_pm("install")
    node_pm("build", "run build")
    os.chdir(tree.root)

def _build_back(root):
    """ """
    tree = ProjectTree(root)

    # Sets up virtual environment
    sh(f"python3.9 -m venv {tree.venv}")
    sh(f"{tree.pip} install -r {tree.requirements}")

    # Processes data and builds model
    process_in  = "twitter-dataset.csv"
    process_out = convert_csv_name(process_in)
    train_out = "twitter-model"

    _process_twitter_data(process_in, process_out)
    train(process_out, train_out, 0, -1, tree.root)

def build(front, back, port, root):
    """ """

    # sassbot build -f
    if front and not back:
        _build_front(port, root)
    # sassbot build -b
    elif back and not front:
        _build_back(root)
    # sassbot build -fb | sassbot build
    else:
        _build_front(port, root)
        _build_back(root)
