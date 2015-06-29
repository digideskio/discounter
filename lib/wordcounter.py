#!/usr/bin/env python

"""
WordCounter class
"""

import logging
import mp_handler
import time
import Queue
from collections import Counter

__author__ = "Fran Fitzpatrick"
__copyright__ = "Copyright (c) 2015, %s" % __author__
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = __author__
__email__ = "francis.x.fitzpatrick@gmail.com"
__status__ = "Prototype"

class WordCounter():
    def __init__(self):
        self.mp = mp_handler.MP_Handler()

    def count(self, files, **kwargs):
        # If it is a worker, go do work!
        if (kwargs["worker"]):
            self.setup_clients(kwargs["ipaddr"],
                               kwargs["port"],
                               kwargs["authkey"],
                               kwargs["nprocs"])
            return

        total_jobs = self.setup_server(kwargs["ipaddr"],
                                       kwargs["port"],
                                       kwargs["authkey"],
                                       files,
                                       kwargs["regex"])

        self.setup_clients(kwargs["ipaddr"],
                           kwargs["port"],
                           kwargs["authkey"],
                           kwargs["nprocs"])

        shared_job_queue = self.server_manager.get_job_queue()
        shared_result_queue = self.server_manager.get_result_queue()
        while shared_result_queue.qsize() != total_jobs:
            pass            

        logging.debug("Items in job queue: %d" % shared_job_queue.qsize())
        logging.debug("Items in result queue: %d" % shared_result_queue.qsize())

        self.print_results(self.sum_results(shared_result_queue)
                           .most_common(kwargs["amt_of_words"]))

        self.server_manager.shutdown()

    def sum_results(self, result_queue):
        logging.debug("Beginning to combine the results queue")
        result = Counter()
        while not result_queue.empty():
            result = result + result_queue.get()
        logging.debug("I have combined the results queue!")
        return result

    def print_results(self, pop_words):
        for i in pop_words:
            print "%s %d" % (i[0], i[1])
    
    def setup_server(self, ip, port, authkey, files, regex):
        """
        Sets up the server, loads it with jobs, and returns how many
        jobs are in the queue.
        """
        self.server_manager = self.mp.make_server_manager(ip, port, authkey)
        shared_job_queue = self.server_manager.get_job_queue()
        
        # TODO: Chunk this up, instead of whole file
        total_jobs = 0
        for f in files:
            shared_job_queue.put([f.read(), regex])
            total_jobs = total_jobs + 1

            # Chunking into each line makes sum_results REALLY slow
            #for line in f:
            #    shared_job_queue.put([line, regex])
            #    total_jobs = total_jobs + 1

        logging.debug("Total jobs in job queue: %s" % total_jobs)
        return total_jobs

    def setup_clients(self, ip, port, authkey, nprocs):
        """
        Sets up the clients/workers, and connects them to the given server
        to begin running jobs
        """
        self.client_manager = self.mp.make_client_manager(ip,
                                                          port,
                                                          authkey)
        self.mp.mp_counter(self.client_manager.get_job_queue(), 
                           self.client_manager.get_result_queue(),
                           nprocs)        
