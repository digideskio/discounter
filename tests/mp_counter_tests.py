import sys
sys.path.insert(0, "../src")

import unittest
import random
import Queue
import time
import multiprocessing
from mp_handler import MP_Handler

class MP_Counter_Tests(unittest.TestCase):
    def setUp(self):
        self.handler = MP_Handler()
        self.regex = "(\w+)" #matches words
        self.manager = self.handler.make_server_manager("127.0.0.1",
                                                   random.randint(44000,55000),
                                                   "test")

    def test_mp_counter_one_file_one_process(self):
        job_queue = self.manager.get_job_queue()
        result_queue = self.manager.get_result_queue()
        nprocs = 1

        file1 = "books/test_map_three_words.txt"
        job_queue.put([file1, 10, self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        self.assertEquals(result_queue.qsize(), 1)

    def test_mp_counter_one_file_eight_processes(self):
        job_queue = self.manager.get_job_queue()
        result_queue = self.manager.get_result_queue()
        nprocs = 8

        file1 = "books/test_map_three_words.txt"
        job_queue.put([file1, 10, self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        self.assertEquals(result_queue.qsize(), 1)

    def test_mp_counter_three_files_eight_processes(self):
        job_queue = self.manager.get_job_queue()
        result_queue = self.manager.get_result_queue()
        nprocs = 8

        file1 = "books/test_map_three_words.txt"
        file2 = "books/test_map_three_words_with_punctuation.txt"
        file3 = "books/test_map_sentence.txt"
        job_queue.put([file1, 10, self.regex])
        job_queue.put([file2, 10, self.regex])
        job_queue.put([file3, 10, self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        self.assertEquals(result_queue.qsize(), 3)

    # TODO: Develop a test to make sure processes are pulling from
    # the job queues correctly so that all jobs are shared accross
    # all of the available processes
        
if __name__ == '__main__':
    unittest.main()

