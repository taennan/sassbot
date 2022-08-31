import tensorflow as tf
from src.ml.models.layers import ProcessText
from unittest import TestCase

class _TestProcessTextLayer(TestCase):
    """ """

    def test_ignore_param(self):
        """ """
        m = ProcessText(lowercase=False, ignore=True)
        self.assertEqual(m._to_lower, True)
        self.assertEqual(m._rm_urls, False)

    def test_converts_to_lowercase(self):
        """ """
        tests = [
            "ABCDE",
            "aB cDE F "
        ]
        expected = tf.convert_to_tensor([
            "abcde",
            "ab cde f ",
        ], dtype=tf.string)
        actual = ProcessText(lowercase=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_replaces_urls(self):
        """ """
        tests = [
            "Go to https://www.whatever.com/fake/url",
            "http://www.fakenews.com is a hoax",
            "Hi, I just came back from www.pointa.com!",
            "The site google.com provides the highest quality education"
        ]
        expected = tf.convert_to_tensor([
            "Go to URL",
            "URL is a hoax",
            "Hi, I just came back from URL",
            "The site URL provides the highest quality education"
        ], dtype=tf.string)
        actual = ProcessText(urls=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_replaces_usernames(self):
        """ """
        tests = [
            "Hello, @username",
            "@twitter-user, bug off! From @insta-user (a troll)",
        ]
        expected = tf.convert_to_tensor([
            "Hello, USER",
            "USER bug off! From USER (a troll)",
        ], dtype=tf.string)
        actual = ProcessText(usernames=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_converts_emojis(self):
        """ """
        tests = [
            "Because I'm :)",
            "I'm having a :( :( day",
        ]
        expected = tf.convert_to_tensor([
            "Because I'm happy",
            "I'm having a sad sad day",
        ], dtype=tf.string)
        actual = ProcessText(emojis=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_removes_symbols(self):
        """ """
        tests = [
            "You'd better watch out!",
            "I'm really ADHD... just joking",
            "(That's a wrap)"
        ]
        expected = tf.convert_to_tensor([
            "Youd better watch out ",
            "Im really ADHD    just joking",
            " Thats a wrap "
        ], dtype=tf.string)
        actual = ProcessText(symbols=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_removes_stopwords(self):
        """ """
        tests = [
            "the quick brown fox jumps over the lazy dog",
            "the most powerful of all the relics",
            "you're really something",
            "yeah, that old thing, it'll go...",
            "we've got a problem cap'n!",
        ]
        expected = tf.convert_to_tensor([
            " quick brown fox jumps over  lazy dog",
            "  powerful    relics",
            " really something",
            "yeah,  old thing,  go...",
            "   problem cap'n!"
        ], dtype=tf.string)
        actual = ProcessText(stopwords=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_removes_numbers(self):
        """ """
        tests = [
            "A2 3 de 220 dsmo 22ij 0",
            "23",
        ]
        expected = tf.convert_to_tensor([
            "A    de     dsmo   ij  ",
            "  ",
        ], dtype=tf.string)
        actual = ProcessText(numbers=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_removes_repeated_words(self):
        """ """
        tests = [
            "I I don't repeat my my myself",
            " do do ray r ay me   me  me  fa sol sola la la te do do    do",
        ]
        expected = tf.convert_to_tensor([
            "I don't repeat my myself",
            " do ray r ay me  fa sol sola la te do",
        ], dtype=tf.string)
        actual = ProcessText(repeated_words=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def test_removes_repeated_chars(self):
        """ """
        tests = [
            "I'm   in a sserious fixxx",
            "Letttterr   writing",
            "There be twain spaces at the end of this sentance!    "
        ]
        expected = [
            "I'm  in a sserious fixx",
            "Letterr  writing",
            "There be twain spaces at the end of this sentance!  "
        ]
        actual = ProcessText(repeated_chars=False, ignore=True)(tests)
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)
