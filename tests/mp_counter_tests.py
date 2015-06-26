import sys
sys.path.insert(0, "../src")

import unittest
import Queue
import time
import multiprocessing
from mp_handler import MP_Handler

class MP_Counter_Tests(unittest.TestCase):
    def setUp(self):
        self.handler = MP_Handler()
        self.regex = "(\w+)" #matches words

    def test_mp_counter_one_file_returns_one_result(self):
        job_queue = multiprocessing.Queue()
        result_queue = multiprocessing.Queue()
        nprocs = 1

        file1 = open("books/test_map_three_words.txt")
        job_queue.put([file1, 10, self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        time.sleep(1)
        
        self.assertEquals(result_queue.qsize(), 1)

#    def test_mp_counter_three_files_returns_three_results(self):
#        job_queue = Queue.Queue()
#        result_queue = Queue.Queue()
#        nprocs = 1
#
#        file1 = open("books/test_map_three_words.txt")
#        file2 = open("books/test_map_three_words_with_punctuation.txt")
#        file3 = open("books/test_map_sentence.txt")
#        job_queue.put([file1, 10, self.regex])
#        job_queue.put([file2, 10, self.regex])
#        job_queue.put([file3, 10, self.regex])
#
#        self.handler.mp_counter(job_queue, result_queue, nprocs)
#        self.assertEquals(result_queue.qsize(), 3)
#
#    def test_mp_counter_three_words_expected_results_correct(self):
#        job_queue = Queue.Queue()
#        result_queue = Queue.Queue()
#        nprocs = 1
#        expected = [('how', 1), ('you', 1), ('are', 1)]
#
#        file1 = open("books/test_map_three_words.txt")
#        job_queue.put([file1, 10, self.regex])
#
#        self.handler.mp_counter(job_queue, result_queue, nprocs)
#
#        self.assertEquals(sorted(result_queue.get().items()[0][1]),
#                          sorted(expected))
        
if __name__ == '__main__':
    unittest.main()

