import sys
sys.path.insert(0, "../src")

import unittest
from mp_handler import MP_Handler

class Popular_Words_Tests(unittest.TestCase):
    def setUp(self):
        self.handler = MP_Handler()

    def test_popular_words_with_three_words(self):
        amt_of_words = 10
        regex = "(\w+)"
        expected = [("how", 1), ("are", 1), ("you", 1)]
        result = self.handler.popular_words("books/"
                                            "test_map_three_words.txt",
                                            amt_of_words,
                                            regex)

        self.assertEquals(sorted(expected), sorted(result))

    def test_popular_words_with_three_words_with_punctuation(self):
        amt_of_words = 10
        regex = "(\w+)"
        expected = [("how", 1), ("are", 1), ("you", 1)]
        result = self.handler.popular_words("books/"
                                            "test_map_three_words_with_"
                                            "punctuation.txt",
                                            amt_of_words,
                                            regex)

        self.assertEquals(sorted(expected), sorted(result))

    def test_popular_words_sentence(self):
        amt_of_words = 5
        regex = "(\w+)"
        expected = [('friend', 2), ('hello', 2), ('i', 2), ('is', 2),
                    ('said', 1)]
        result = self.handler.popular_words("books/"
                                            "test_map_sentence.txt",
                                            amt_of_words,
                                            regex)

        self.assertEquals(sorted(expected), sorted(result))
        
if __name__ == '__main__':
    unittest.main()

