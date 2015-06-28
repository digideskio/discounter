import logging
import mp_handler
import time
import Queue
from collections import Counter

class WordCounter():
    def count(self, files, **kwargs):
        mp = mp_handler.MP_Handler()
        server_manager = mp.make_server_manager("127.0.0.1", 45329, "test")
        shared_job_queue = server_manager.get_job_queue()
        shared_result_queue = server_manager.get_result_queue()

        # TODO: Chunk this up, instead of whole file
        total_jobs = 0
        for f in files:
            shared_job_queue.put([f.read(), kwargs["regex"]])
            total_jobs = total_jobs + 1

        client_manager = mp.make_client_manager("127.0.0.1", 45329, "test")
        mp.mp_counter(client_manager.get_job_queue(), 
                      client_manager.get_result_queue(),
                      kwargs["nprocs"])        

        while shared_result_queue.qsize() != total_jobs:
            pass            

        logging.debug("Items in job queue: %d" % shared_job_queue.qsize())
        logging.debug("Items in result queue: %d" % shared_result_queue.qsize())

        self.print_results(self.sum_results(shared_result_queue).most_common(kwargs["amt_of_words"]))

        server_manager.shutdown()

    def sum_results(self, result_queue):
        result = Counter()
        while not result_queue.empty():
            result = result + result_queue.get()
        return result

    def print_results(self, pop_words):
        for i in pop_words:
            print "%s %d" % (i[0], i[1])
