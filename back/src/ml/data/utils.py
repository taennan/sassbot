import math
from pathlib import Path

import numpy as np
import pandas as pd

# Had t specify paths like so for the notebooks
DATA_DIR     = Path(__file__).parent / "processed"
RAW_DATA_DIR = Path(__file__).parent / "unprocessed"

# The column names used by our pandas dataframes
DATA_COLS = ["text", "sentiment"]

def load_df(file, slice=None, shuffle=False):
    """
    Returns ``pandas.DatFrame`` from specified csv file

    Parameters
    ----------
    file : pathlike
    slice : int | tuple | list, optional
    shuffle : bool | str, optional

    Returns
    -------
    pandas.DataFrame
    """

    # Allows 'file' arg to be specified only with
    # the stem of the csv file within 'DATA_DIR'
    file = Path(file)
    if file.parent != DATA_DIR:
        file = DATA_DIR / file
    if file.suffix != ".csv":
        file = file.parent / f"{file.stem}.csv"

    df = pd.read_csv(file, names=DATA_COLS)
    df = df.dropna(how="any")

    # Shuffles before slicing
    if shuffle == "before" or shuffle == "pre":
        df = df.sample(frac=1)

    # Slices from start to 'slice'
    if isinstance(slice, int):
        max_each = slice // 2
        pos = df[df.sentiment == 1][:max_each]
        neg = df[df.sentiment == 0][:max_each]
        df = pd.concat([pos, neg])
    # Slices from slice[0]th to slice[1]th
    elif isinstance(slice, tuple) or isinstance(slice, list):
        a = slice[0] // 2
        b = slice[1] // 2
        pos = df[df.sentiment == 1][a:b]
        neg = df[df.sentiment == 0][a:b]
        df = pd.concat([pos, neg])

    # Shuffles after slicing
    if shuffle is True or shuffle == "after" or shuffle == "post":
        df = df.sample(frac=1)

    #if slice is not None:
    #    max_each = slice // 2
    #    pos = df[df["sentiment"] == 1][:max_each]
    #    neg = df[df["sentiment"] == 0][:max_each]
    #    df = pd.concat([pos, neg])
    #if shuffle:
    #    df = df.sample(frac=1)

    return df

def data_split(x, y, ratios, shuffle=False) -> list:
    """
    Data Train, Test and Validation split

    Parameters
    ----------

    x : list
    y : list
    ratios: list[float | int]
        Floats used to determine the ratios of the data split.
        The length of this param determines the length of the return value.
        All numbers within this param must add up to 1
    shuffle : bool
        Shuffles ``x`` and ``y`` with the same permutation before splitting.
        It is advised to preset ``numpy.random.seed`` for reproducible results

    Returns
    -------

    List of length inferred from ``ratios`` containing tuples of the split data

    Examples
    --------

    >>> # Basic usage
    >>> (x_train, y_train), (x_test, y_test), (x_val, y_val) = data_split(x, y, [0.8, 0.1, 0.1])

    >>> # Or...
    >>> train, test = data_split(x, y, [0.8, 0.2])
    """
    #
    assert len(x) == len(y), f"Expected lengths of 'x' and 'y' to be equal, got {len(x)} and {len(y)} respectively"
    assert math.fsum(ratios) == 1, f"Expected 'ratios' to add up to 1, sum of 'ratios' equals {math.fsum(ratios)}"

    if shuffle:
        perm = np.random.permutation(len(x))
        x = x[perm]
        y = y[perm]

    split = []
    last_i  = 0
    for r in ratios:
        i = last_i + int(len(x) * r)
        split.append((
            x[last_i:i],
            y[last_i:i]
        ))
        last_i = i

    return split
