import sys
from pathlib import Path

import tensorflow as tf
import pandas as pd
from pandas import DataFrame

from utils import ProjectTree, add_prj_module
add_prj_module("ml")
from data import load_df
from model import make_model
from layers import ProcessText


def _train_model(dataset_name, out, start, stop, root):
    """ """
    tree = ProjectTree(root)

    print(f"Training model on {dataset_name} dataset...")

    df = load_df(dataset_name, shuffle=True)
    # Gets 'start' to 'stop' rows of df
    stop = len(df) if stop < 0 else stop
    df = df[start:stop]

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
    )

    tree.saved_models.mkdir(exist_ok=True)
    model.save(tree.saved_models / out)

    print(f"Saved trained model to {out}")

def train(in_, out, start, stop, root):
    """ """
    print(in_, out, start, stop, root)
    #_train_model(in_, out, start, stop, root)
