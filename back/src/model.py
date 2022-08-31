import random as rand
from pathlib import Path
from time import time

import tensorflow as tf

import responses as res
from ml.models.layers import ProcessText
from utils import ROOT_DIR

_model = tf.keras.models.load_model(ROOT_DIR / "tf_model")

def predict(text: str) -> float:
    """Returns model predictions"""
    # Have to process here as the repeated chars and words
    #  steps couldn't be serialised in the saved model
    text = ProcessText(
        repeated_chars=False,
        repeated_words=False,
        ignore=True
    )([text])
    # Have to do a bunch of conversions to get the single float value
    pred = float(list(_model.predict(text))[0][0])
    return pred

def polarize(pred: float, margin=0.5):
    """ """
    if pred > margin:
        return True
    return False

def generate_response_json(input: str) -> dict:
    """
    [Description]

    Returns
    -------
    dict
        input : str
        output : str
        is_polite : bool
        prediction : float
        prediction_time : float
    """

    t = time()
    pred = predict(input)
    t = time() - t

    is_polite = polarize(pred)

    return {
        "input": input,
        "output": res.random_response(is_polite),
        "is_polite": is_polite,
        "prediction": pred,
        "prediction_time": t,
    }
