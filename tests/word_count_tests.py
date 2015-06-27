import sys
sys.path.insert(0, "../src")

import unittest
from collections import Counter
from mp_handler import MP_Handler


class Word_Count_Tests(unittest.TestCase):
    def setUp(self):
        self.handler = MP_Handler()

    def test_word_count_with_three_words(self):
        regex = "(\w+)"
        expected = Counter(['how','you','are'])
        filename = "books/test_map_three_words.txt"
        result = self.handler.word_count(open(filename).read(),
                                            regex)

        self.assertEquals(expected, result)

    def test_word_count_with_three_words_with_punctuation(self):
        regex = "(\w+)"
        expected = Counter(['how','you','are'])
        filename = "books/test_map_three_words_with_punctuation.txt"
        result = self.handler.word_count(open(filename).read(),
                                            regex)

        self.assertEquals(expected, result)

    def test_word_count_sentence(self):
        regex = "(\w+)"
        expected = Counter({'i': 2, 'is': 2, 'hello': 2, 'friend': 2,
                            'said': 1, 'name': 1, 'her': 1, 'fran': 1,
                            'there': 1, 'well': 1, 'your': 1, 'doing': 1,
                            'jaime': 1, 'hope': 1, 'tell': 1, 'my': 1})
        filename = "books/test_map_sentence.txt"
        result = self.handler.word_count(open(filename).read(),
                                            regex)

        self.assertEquals(expected, result)

if __name__ == '__main__':
    unittest.main()

