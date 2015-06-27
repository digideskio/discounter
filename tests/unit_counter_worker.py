import sys
sys.path.insert(0, "../src")

import unittest
import Queue
from mp_handler import MP_Handler
from collections import Counter

class Counter_Worker_Tests(unittest.TestCase):
    def setUp(self):
        self.handler = MP_Handler()
        self.regex = "(\w+)" #matches words

    def test_counter_worker_one_file_returns_one_result(self):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()

        file1 = "books/test_map_three_words.txt"
        job_queue.put([open(file1).read(), self.regex])

        self.handler.counter_worker(job_queue, result_queue)
        self.assertEquals(result_queue.qsize(), 1)

    def test_counter_worker_three_files_returns_three_results(self):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()

        file1 = "books/test_map_three_words.txt"
        file2 = "books/test_map_three_words_with_punctuation.txt"
        file3 = "books/test_map_sentence.txt"
        job_queue.put([open(file1).read(), self.regex])
        job_queue.put([open(file2).read(), self.regex])
        job_queue.put([open(file3).read(), self.regex])

        self.handler.counter_worker(job_queue, result_queue)
        self.assertEquals(result_queue.qsize(), 3)

    def test_counter_worker_three_words_expected_results_correct(self):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()
        expected = Counter(['how','you','are'])

        file1 = "books/test_map_three_words.txt"

        job_queue.put([open(file1).read(), self.regex])

        self.handler.counter_worker(job_queue, result_queue)

        self.assertEquals(result_queue.get(), expected)

        
if __name__ == '__main__':
    unittest.main()

