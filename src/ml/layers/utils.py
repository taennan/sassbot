from tensorflow.data import Dataset
from tensorflow.keras.layers import (
    TextVectorization,
    Bidirectional,
    SimpleRNN,
    LSTM,
    GRU,
)

def convert_dense_units(units):
    """ """
    return [int(s) for s in units.split()]

def txt_vec_layer(vocab, max_tokens, out_sequence_len, batch_size=64):
    """ """
    txt_vec = TextVectorization(
        max_tokens             = max_tokens,
        output_sequence_length = out_sequence_len,
    )
    # Batching noticeably improves performance on large datasets
    ds = Dataset.from_tensor_slices(vocab)
    txt_vec.adapt(ds.batch(batch_size))

    return txt_vec

def rnn_layer(rnn, units, **kwargs):
    """ """
    if rnn == "simple":
        return SimpleRNN(units, **kwargs)
    elif rnn == "lstm":
        return LSTM(units, **kwargs)
    elif rnn == "gru":
        return GRU(units, **kwargs)
    else:
        raise ValueError(f"Unknown arg '{typ}' for hparam 'rnn'. Expected one of 'simple', 'lstm' or 'gru'")

def bi_rnn_layer(rnn, units, **kwargs):
    """ """
    ret_seq = kwargs.get("return_sequences", False)
    inp_shp = kwargs.get("input_shape")

    rnn = rnn_layer(rnn, units, return_sequences=ret_seq)
    if inp_shp is not None:
        return Bidirectional(rnn, input_shape=inp_shp)
    return Bidirectional(rnn)
