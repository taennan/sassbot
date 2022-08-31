from pathlib import Path
from collections import namedtuple

from .utils import data_split

XY = namedtuple("XY", ["x", "y"])

class Data:
    """ """

    @classmethod
    def from_xy(cls, x, y, split):
        """ """
        return Data(*data_split(x, y, split))

    @classmethod
    def from_df(cls, df, split, shuffle=False):
        """ """
        if shuffle:
            df = df.sample(frac=-1)
        return Data.from_xy(df.text, df.sentiment, split)

    @classmethod
    def from_csv(cls, file, split, max_samples=None, shuffle=False):
        """ """
        df = load_df(file, max_samples, shuffle)
        return Data.from_xy(df.text, df.sentiment)

    def __init__(self, trn, tst, val=None):
        """ """
        self.trn = XY(*trn)
        self.tst = XY(*tst)
        self.val = None if val is None else XY(*val)
