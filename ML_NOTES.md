
# Experimentation Notes

Experimentation is ongoing. What follows are the results of a few early tests.

## Data

Multiple datasets were used in the experiments, namely:
- Imdb Text Sentiment (`1000` samples)
- Yelp Text Sentiment (`1000` samples)
- Amazon Text Sentiment (`1000` samples)
- Twitter Tweets (`1.6M` samples)

The first 3 datasets were used mainly for testing and validation, as they were
far cleaner and closer to real life cases.
Unfortunately, there source cannot be remembered. Apologies to any who wish to
reproduce my results

Due to the small sizes of the first datasets, the final model was trained on
`TODO` samples of the larger [twitter dataset][twitter-dataset].
That dataset was obtained from [Kaggle][kaggle].

## Hyper Parameter Tuning

The [`keras_tuner`][keras-tuner-github]'s `Hyperband` tuner was used to assess the most efficient values
for:
- Removal of common English words
- Max tokens of text vectorization
- Sequence length of text vectorization
- Output length of embedding layer
- RNN model
- Number of bidirectional RNN layers
- Number of hidden layers
- Units assigned to each dense layer
- Activation functions for hidden layers
- Dropout between hidden layers

### Tuning Methods

Tuning was split into 2 parts, namely:
- RNN tuning
- Hidden layer tuning

This was done on the (probably inaccurate) understanding that Data Preprocessing,
Text Vectorization, Embedding and Bidirectional RNNs would learn the features
of the data, while the Hidden Layers would draw boundaries between
their outputs in order to make more detailed classifications.

Early tuning was done on the smaller `Imdb`, `Yelp` and `Amazon` datasets while
the final tuning and testing was conducted with slices of the `Twitter` dataset.

##### RNN Tuning

RNN tuning was conducted without _any_ hidden layers in order to reduce the
hyperspace area the `Hyperband` tuner would have to search.

Multiple architectures were tried, including:
- Single RNN
- Multiple RNNs
- Multiple Bidirectional RNNs
- Multiple Bidirectional RNNs fed into 2D Convolutional and MaxPooling layers

It was quickly found that relatively better results were obtained from multiple.
bidirectional RNN layers, which tended to give results within `70...75%`
validation accuracy in early experiments.

##### Hidden Layer Tuning

The best models found by the RNN Tuning step had hidden layers added to them in
order to find best hyper parameters for the complete model.

### Parameters with Profound Impact

The following were found during tuning with the small datasets.
Results may differ on larger datasets.

##### Removal of Common Words

It was found that removing common English words usually resulted in slightly
better models. Common words that could invert the meaning of a sentence or could
be used in positive or negative connotations by themselves were not removed.

##### Max Tokens

On the small datasets, it was found that models performed better with this value
set within `1200...1800`, with the best being within `1700...1800`.

##### RNN Type and Layers

Most models performed better with `3...4` Bidirectional `LSTM` layers.
Although some `2` layered and/or `GRU` based models seemed to perform marginally
well with larger sequence and embedding lengths.

## Final Model Architecture and Statistics

TODO

[kaggle]: https://www.kaggle.com
[twitter-dataset]: https://www.kaggle.com/datasets/kazanova/sentiment140

[keras-tuner-github]: https://github.com/keras-team/keras-tuner
