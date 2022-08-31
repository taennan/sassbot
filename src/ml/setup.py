"""
Setup script for preprocessing data and training algorithms

Usage:
  setup.py model --data <data> [--out <out>]
  setup.py process --data <data> [--out <out>]

Options:
  -d <data>, --data  <data>  XXX
  -o <out>, --out <out>  Leave as '' to ignore [default: '']

"""

from pathlib import Path

import tensorflow as tf
from tensorflow.keras.callbacks import ReduceLROnPlateau
import pandas as pd
from pandas import DataFrame
from stringth import neg_to_inf
from docopt import docopt

from data import load_df, DATA_COLS, DATA_DIR, RAW_DATA_DIR
from model import make_model
from models.layers import ProcessText

MODEL_SAVE_DIR = Path(__file__).parent.parent / "models"

def convert_raw_csv_stem(full_path):
    """ """
    sffx = ""
    for s in full_path.suffixes:
        sffx += s
    stem = Path(full_path).stem
    stem = stem.removesuffix("-unprocessed")
    return full_path.parent / f"{stem}-processed{sffx}"

def build_model(dataset, out):
    """ """

    print(f"Training model on {DATA_DIR / dataset} dataset...")

    df = load_df(dataset, shuffle=True)
    X, Y = df.text, df.sentiment

    model = make_model(
        vocab = X.values,
        max_tokn = 1750,
        seq_len  = 80,
        emb_len  = 60,
        rnn        = "lstm",
        rnn_layers = 3,
        dns_units = "60 60 30",
        dns_drop  = 0.4,
        dns_actv  = "relu",
    )
    model.fit(
        X, Y,
        epochs=12,
        callbacks=[
            #ReduceLROnPlateau("val_accuracy", patience=5, factor=0.2),
        ]
    )

    MODEL_SAVE_DIR.mkdir(exist_ok=True)
    save_path = MODEL_SAVE_DIR / out or "tf_model"
    model.save(save_path)

    print(f"Saved trained model to {MODEL_SAVE_DIR}")

def process_data(dataset, out):
    """Processes the large twitter dataset from scratch"""

    print(f"Processing dataset at {RAW_DATA_DIR / dataset}...")

    encoding = "ISO-8859-1"
    cols = ["sentiment", "id", "date", "flag", "user", "text"]

    df = pd.read_csv(RAW_DATA_DIR / dataset, names=cols)

    # Drops any columns not named 'text' or 'sentiment'
    df = df.drop(columns=[c for c in df.columns if c not in DATA_COLS])
    df = df.reindex(columns=DATA_COLS)
    df = df.drop_duplicates(subset="text")
    # Sets values of positive rows to 1 since
    #  they're listed as 4 for some reason
    df.sentiment = df.sentiment.replace(4,1)

    df.text = ProcessText()(df.text.values).numpy()
    df.text = df.text.apply(lambda i: i.decode())

    if out:
        save_path = DATA_DIR / out
    else:
        save_path = convert_raw_csv_stem(DATA_DIR / dataset)
    df.to_csv(save_path, header=False, index=False)

    print(f"Saved processed dataset to {save_path}")

if __name__ == "__main__":
    args = docopt(__doc__, version="0.0.1")

    d, o = (
        args["--data"],
        args["--out"],
    )

    if args["process"]:
        process_data(d, o)
    elif args["model"]:
        build_model(d, o)
