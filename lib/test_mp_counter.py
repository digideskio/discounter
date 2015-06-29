import unittest
import random
import Queue
import time
import multiprocessing
from collections import Counter
from mp_handler import MP_Handler

class MP_Handler_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.handler = MP_Handler()
        self.regex = "(\w+)"

    def setUp(self):
        self.manager = self.handler.make_server_manager("127.0.0.1",
                                                        random.randint(44000,
                                                                       55000),
                                                        "testkey")

    def test_word_count_with_three_words(self):
        expected = Counter(['how','you','are'])
        filename = "test_artifacts/test_map_three_words.txt"
        result = self.handler.word_count(open(filename).read(),
                                         self.regex)

        self.assertEquals(expected, result)
        
    def test_word_count_with_three_words_with_punctuation(self):
        expected = Counter(['how','you','are'])
        filename = "test_artifacts/test_map_three_words_with_punctuation.txt"
        result = self.handler.word_count(open(filename).read(),
                                         self.regex)

        self.assertEquals(expected, result)

    def test_word_count_sentence(self):
        expected = Counter({'i': 2, 'is': 2, 'hello': 2, 'friend': 2,
                            'said': 1, 'name': 1, 'her': 1, 'fran': 1,
                            'there': 1, 'well': 1, 'your': 1, 'doing': 1,
                            'jaime': 1, 'hope': 1, 'tell': 1, 'my': 1})
        filename = "test_artifacts/test_map_sentence.txt"
        result = self.handler.word_count(open(filename).read(),
                                         self.regex)

        self.assertEquals(expected, result)

    def test_counter_worker_one_file_returns_one_result(self):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()

        file1 = "test_artifacts/test_map_three_words.txt"
        job_queue.put([open(file1).read(), self.regex])

        self.handler.counter_worker(job_queue, result_queue)
        self.assertEquals(result_queue.qsize(), 1)

    def test_counter_worker_three_files_returns_three_results(self):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()

        file1 = "test_artifacts/test_map_three_words.txt"
        file2 = "test_artifacts/test_map_three_words_with_punctuation.txt"
        file3 = "test_artifacts/test_map_sentence.txt"
        job_queue.put([open(file1).read(), self.regex])
        job_queue.put([open(file2).read(), self.regex])
        job_queue.put([open(file3).read(), self.regex])

        self.handler.counter_worker(job_queue, result_queue)
        self.assertEquals(result_queue.qsize(), 3)

    def test_counter_worker_three_words_expected_results_correct(self):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()
        expected = Counter(['how','you','are'])

        file1 = "test_artifacts/test_map_three_words.txt"

        job_queue.put([open(file1).read(), self.regex])

        self.handler.counter_worker(job_queue, result_queue)

        self.assertEquals(result_queue.get(), expected)

    def test_mp_counter_one_file_one_process(self):
        job_queue = self.manager.get_job_queue()
        result_queue = self.manager.get_result_queue()
        nprocs = 1

        file1 = "test_artifacts/test_map_three_words.txt"
        job_queue.put([open(file1).read(), self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        self.assertEquals(result_queue.qsize(), 1)

    def test_mp_counter_one_file_eight_processes(self):
        job_queue = self.manager.get_job_queue()
        result_queue = self.manager.get_result_queue()
        nprocs = 8

        file1 = "test_artifacts/test_map_three_words.txt"
        job_queue.put([open(file1).read(), self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        self.assertEquals(result_queue.qsize(), 1)
        
    def test_mp_counter_three_files_eight_processes(self):
        job_queue = self.manager.get_job_queue()
        result_queue = self.manager.get_result_queue()
        nprocs = 8

        file1 = "test_artifacts/test_map_three_words.txt"
        file2 = "test_artifacts/test_map_three_words_with_punctuation.txt"
        file3 = "test_artifacts/test_map_sentence.txt"
        job_queue.put([open(file1).read(), self.regex])
        job_queue.put([open(file2).read(), self.regex])
        job_queue.put([open(file3).read(), self.regex])

        self.handler.mp_counter(job_queue, result_queue, nprocs)

        self.assertEquals(result_queue.qsize(), 3)

    # TODO: Develop a test to make sure processes are pulling from
    # the job queues correctly so that all jobs are shared accross
    # all of the available processes
        
if __name__ == '__main__':
    unittest.main()
