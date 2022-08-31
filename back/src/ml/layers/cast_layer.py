import tensorflow as tf
from tensorflow.keras.layers import Layer

class Cast(Layer):
    """Converts elements of inputs to data type specified"""
    def __init__(self, t):
        super().__init__()
        self.t = t

    def call(self, inputs):
        return tf.cast(inputs, dtype=tf.float32)
        #return tf.convert_to_tensor(inputs, dtype=self.t)

    def get_config(self):
        """ """
        return {
            **super().get_config(),
            "t": self.t,
        }
