import unittest
import pep8


class Pep8_Tests(unittest.TestCase):
    def test_pep8_self(self):
        self.assertEquals(pep8.Checker(__file__).check_all(), 0)

    def test_pep8_mp_handler(self):
        self.assertEquals(pep8.Checker("mp_handler.py").check_all(), 0)

    def test_pep8_wordcounter(self):
        self.assertEquals(pep8.Checker("wordcounter.py").check_all(), 0)

    def test_pep8_main(self):
        self.assertEquals(pep8.Checker("../main.py").check_all(), 0)

if __name__ == '__main__':
    unittest.main()
