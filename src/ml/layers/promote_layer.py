import tensorflow as tf
from tensorflow.keras.layers import Layer

class Promote(Layer):
    """ """

    def call(self, inputs):
        """ """
        out_shape = (-1, *inputs.shape[1:], 1)
        return tf.reshape(inputs, out_shape)
