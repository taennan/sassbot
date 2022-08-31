import re

import numpy as np
import tensorflow as tf
from tensorflow.strings import regex_replace, lower
from tensorflow.keras.layers import Layer

SYMBOLS = [
    r"\.", ",", r"\:", ";", r"\(", r"\)", r"\!", r"\?", r"\$", r"\=", r"\+",
    r"\-", "/", r"\*", "&", "#", "@", "%", r"\^", "~", r"\<", r"\>", r"\|",
    r"\\", "'",
]

# NOTE:
# Put the apostrophe-able and least matchable words first
# "i'd" and "i'll" are intentional as putting a '? in them will match ID and ILL
# Will not include 't' as that spoils negative words like 'didn't', 'don't ', etc
# Will not include the following due the way they may be used in positive or negative sentances:
# - should've
# - wouldn't
# - can't
# - ain't
# - down
# - above
# - until
STOPWORDS = [
    "a", "about", "after", "again", "all", "am", "an",
    "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between","both", "by",
    "can",
    "did", "do", "does", "doing", "during",
    "each",
    "few", "for", "from", "further",
    "get", "got",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how",
    "it'?s", "it'?ll", "i'll", "i'd", "i'?m", "i'?ve", "if", "in", "into",
    "is", "it", "itself", "i",
    "just",
    "me", "more", "most", "my", "myself",
    "now",
    "o", "of", "on", "once", "only", "or", "other", "our", "ours", "ourselves",
    "out", "own",
    "she'?s", "same", "she", "should", "so", "some", "such", "s",
    "that'?ll", "than", "that",  "the", "their", "theirs", "them",
    "themselves", "then", "there", "these", "they", "this", "those",
    "through", "too", "to",
    "up", "u",
    "very",
    "we'?re", "we'?ve", "what", "when", "where", "which", "while", "whom", "who",
    "was", "we", "why", "will", "with",
    "you'?d", "you'?ll", "you'?re", "you'?ve", "your", "yours", "yourself",
    "yourselves", "you", "y",

    # These are special, they pick out any straggler apostrophe-able words
    # As such, they MUST COME LAST
    "re", "ll", "ve", "d", "m",
]

EMOJIS = {
    r":\)": 'happy',
    r":-\)": 'happy',
    r";d": 'wink',
    r":-E": 'vampire',
    r":\(": 'sad',
    r":-\(": 'sad',
    r":-<": 'sad',
    r":P": 'raspberry',
    r":O": 'surprised',
    r":-@": 'shocked',
    r":@": 'shocked',
    r":-\$": 'confused',
    r":\\": 'annoyed',
    r":#": 'mute',
    r":X": 'mute',
    r":\^\)": 'smile',
    r":-&": 'confused',
    r"\$_\$": 'greedy',
    r"@@": 'eyeroll',
    r":-!": 'confused',
    r":-D": 'smile',
    r":-0": 'yell',
    r"O\.o": 'confused',
    r"<\(-_-\)>": 'robot',
    r"d\[-_-\]b": 'dj',
    r":'-\)": 'sadsmile',
    r";\)": 'wink',
    r";-\)": 'wink',
    r"O:-\)": 'angel',
    r"O\*-\)": 'angel',
    r"\(:-D": 'gossip',
    r"=\^\.\^=": 'cat'
}

def _build_regex_options(*options, pre="", post=""):
    """
    Returns an optional regex pattern

    Pattern returned is in the form '(option_1|option_2|option_3)'
    """
    pttn = "("
    for i, word in enumerate(options):
        pttn += f"{pre}{word}{post}"
        if i != len(options) - 1:
            pttn += "|"
    pttn += ")"
    return pttn

def _convert_str_tensor_item(item, encoding=tf.int16, fixed_length=1000):
    """
    Needed to convert an ``str`` element of a ``tensorflow.Tensor`` into a form we can work with
    """
    text = tf.io.decode_raw(item, encoding, fixed_length=fixed_length)
    text = bytes(text).decode().rstrip(bytes([0]).decode())
    return text


def _process_case(inputs):
    """ """
    return lower(inputs)

def _process_urls(inputs):
    """ """
    pttn = r"(?:https?://[^\s]+)|(www\.[^\s]+)|(\b\w+\.(com|fj|au|us|nz|uk)\b)"
    repl = r"URL"
    return regex_replace(inputs, pttn, repl)

def _process_usernames(inputs):
    """ """
    pttn = r"@[^\s]+"
    repl = r"USER"
    return regex_replace(inputs, pttn, repl)

def _process_emojis(inputs):
    """ """
    for emoji, meaning in EMOJIS.items():
        inputs = regex_replace(inputs, emoji, meaning)
    return inputs

def _process_symbols(inputs):
    """ """
    for symbol in SYMBOLS:
        # Replaced all apostrophes with an empty string to
        #  condense words like don't, won't, etc.
        # Everything else is replaced with a space in case proper spacing was
        #  not used during punctuation of the sentance
        repl = "" if symbol == "'" else " "
        inputs = regex_replace(inputs, symbol, repl)
    return inputs

def _process_numbers(inputs):
    """ """
    # Replaced with a space in case numbers were put right next to letters
    return regex_replace(inputs, r"\d", " ")

def _process_stopwords(inputs):
    """ """
    pttn = _build_regex_options(*STOPWORDS, pre=r"\b", post=r"\b")
    return regex_replace(inputs, pttn, "")


def _process_repeated_words(inputs):
    """ """
    def rm_repeated_words(args):
        """ """
        output = []
        for item in args:
            pttn = r"\b(\w+)(\s+\1\b)+"
            repl = r"\1"
            # Google's RE2 engine doesn't handle backcapturing (or whatever it's called)
            #  so we have to use the 're' module instead
            # This does have the disadvantage of making the layer non-serializable
            #  when saving
            output.append(re.sub(pttn, repl, _convert_str_tensor_item(item)))
        return tf.convert_to_tensor(output)

    return tf.py_function(rm_repeated_words, [inputs], tf.string)

def _process_repeated_chars(inputs):
    """ """
    def rm_repeated_chars(args):
        """ """
        output = []
        for item in args:
            pttn = r"(.)\1\1+"
            repl = r"\1\1"
            # See '_process_repeated_words' above for notes on this implementation
            output.append(re.sub(pttn, repl, _convert_str_tensor_item(item)))
        return tf.convert_to_tensor(output)

    return tf.py_function(rm_repeated_chars, [inputs], tf.string)


class ProcessText(Layer):
    """ """

    def __init__(self,
        lowercase=True,
        urls=True,
        usernames=True,
        emojis=True,
        symbols=True,
        numbers=True,
        stopwords=True,
        repeated_words=True,
        repeated_chars=True,
        ignore=False):
        """
        Parameters
        ----------
        repeated_words : bool, optional
            Leave as False if model is needed to be saved
        repeated_chars : bool, optional
            Leave as False if model is needed to be saved

        Other Parameters
        ----------------
        ignore : bool, optional
            Flips the bool value of all other parameters.
            Defaults to False
        """
        super().__init__()

        def not_if(x, condition):
            """Applies NOT operator to ``x`` if ``condition`` is True"""
            return x if not condition else not x

        self._to_lower          = not_if(lowercase,      ignore)
        self._rm_urls           = not_if(urls,           ignore)
        self._rm_usernames      = not_if(usernames,      ignore)
        self._rm_emojis         = not_if(emojis,         ignore)
        self._rm_symbols        = not_if(symbols,        ignore)
        self._rm_numbers        = not_if(numbers,        ignore)
        self._rm_stopwords      = not_if(stopwords,      ignore)
        self._rm_repeated_words = not_if(repeated_words, ignore)
        self._rm_repeated_chars = not_if(repeated_chars, ignore)

        self._ignores = ignore

    def compute_output_shape(self, input_shape):
        """ """
        return tf.convert_to_tensor((-1, 1))

    def call(self, inputs):
        """ """
        if self._to_lower:
            inputs = _process_case(inputs)
        if self._rm_urls:
            inputs = _process_urls(inputs)
        if self._rm_usernames:
            inputs = _process_usernames(inputs)
        if self._rm_emojis:
            inputs = _process_emojis(inputs)
        if self._rm_symbols:
            inputs = _process_symbols(inputs)
        if self._rm_numbers:
            inputs = _process_numbers(inputs)
        if self._rm_stopwords:
            inputs = _process_stopwords(inputs)
        if self._rm_repeated_words:
            inputs = _process_repeated_words(inputs)
        if self._rm_repeated_chars:
            inputs = _process_repeated_chars(inputs)

        return tf.reshape(inputs, self.compute_output_shape(inputs.shape))

    def get_config(self):
        """ """
        return {
            **super().get_config(),
            "lowercase": self._to_lower,
            "urls": self._rm_urls,
            "usernames": self._rm_usernames,
            "emojis": self._rm_emojis,
            "symbols": self._rm_symbols,
            "numbers": self._rm_numbers,
            "stopwords": self._rm_stopwords,
            "repeated_words": self._rm_repeated_words,
            "repeated_chars": self._rm_repeated_chars,
            "ignore": self._ignores,
        }
