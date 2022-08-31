import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.losses import BinaryCrossentropy as BCE
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import (
    Input,
    TextVectorization,
    Embedding,
    Dropout,
    Dense,
)

from layers import (
    ProcessText,
    txt_vec_layer,
    bi_rnn_layer,
    convert_dense_units,
)

def make_model(
    vocab,
    #
    max_tokn,
    seq_len,
    emb_len,
    #
    rnn,
    rnn_layers,
    #
    dns_drop,
    dns_units,
    dns_actv,
    #
    compile=True,
    verbose=1):
    """
    [Description]

    Parameters
    ----------
    vocab : list[str]
    max_tokn : int
    seq_len : int
    emb_len : int
    rnn : str
        The RNN architecture to use within the model.
        One of 'simple', 'lstm' or 'gru'.
    rnn_layers : int
    dns_drop : float
    dns_units : str
        The number or hidden layers and units for each layer to use.
        E.G:
        - '512 512 10' makes 3 Dense layers with 512, 512 and 10 units respectively
    dns_actv : str
        Activation function for use by hidden layers.
        See ``tensorflow.keras.layers.Dense`` for possible variations.
        To set the value to ``None``, pass an empy string ('')
    compile : bool, optional
        Call ``model.compile()`` on built model before returning.
        Defaults to ``True``.
    verbose : int, optional
        If set above 0, will print model summary on compilation

    Returns
    -------
    tensorflow.keras.models.Model
        The compiled (if specified) model built with the above hyper parameters
    """

    inp = Input((1,), dtype=tf.string)
    x = ProcessText(
        repeated_chars=False,
        repeated_words=False
    )(inp)
    x = txt_vec_layer(vocab, max_tokn, seq_len)(x)
    x = Embedding(
        # Add 1 to max_tokens as they are zero indexed
        input_dim    = max_tokn + 1,
        output_dim   = emb_len,
        input_length = seq_len
    )(x)
    for i in range(rnn_layers):
        ret_seqs = False if i == rnn_layers - 1 else True
        if i == 0:
            inp_shp = (None, seq_len, emb_len)
            x = bi_rnn_layer(rnn, emb_len, input_shape=inp_shp, return_sequences=ret_seqs)(x)
        else:
            x = bi_rnn_layer(rnn, emb_len, return_sequences=ret_seqs)(x)
    for u in convert_dense_units(dns_units):
        x = Dropout(dns_drop)(x)
        x = Dense(u, dns_actv or None)(x)
    out = Dense(1, "sigmoid")(x)

    model = Model(inp, out)

    if compile:
        model.compile(
            optimizer=Adam(),
            loss=BCE(from_logits=False),
            metrics=["accuracy"]
        )
        if verbose > 0:
            print(model.summary())

    return model
