import tensorflow as tf
from tensorflow.keras.layers import Layer

class Scale(Layer):
    """ """

    def __init__(self, min=0, max=1):
        super().__init__()
        self.min = min
        self.max = max

    def call(self, inputs):
        repeat = inputs.shape[1]
        xmin = tf.repeat(
            tf.reshape(tf.math.reduce_min(inputs, axis=1), shape=[-1,1]),
            repeats=repeat,
            axis=1
        )
        xmax = tf.repeat(
            tf.reshape(tf.math.reduce_max(inputs, axis=1), shape=[-1,1]),
            repeats=repeat,
            axis=1
        )
        return (inputs - xmin) / (xmax - xmin)

    def get_config(self):
        """ """
        return {
            **super().get_config(),
            "min": self.min,
            "max": self.max,
        }
