#!/usr/bin/env python

"""
Multiprocessing handler used for the word counter application
"""

import logging
import time
import re
import multiprocessing
import sys
from functools import partial
from multiprocessing.managers import SyncManager
from collections import Counter
from Queue import Queue as RealQueue
from Queue import Empty

__author__ = "Fran Fitzpatrick"
__copyright__ = "Copyright (c) 2015, %s" % __author__
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = __author__
__email__ = "francis.x.fitzpatrick@gmail.com"
__status__ = "Prototype"


class Queue(RealQueue):
    """ A picklable queue """
    def __getstate__(self):
        return (self.maxsize, self.queue, self.unfinished_tasks)

    def __setstate__(self, state):
        Queue.__init__(self)
        self.maxsize = state[0]
        self.queue = state[1]
        self.unfinished_tasks = state[2]

class JobQueueManager(SyncManager):
    pass

def get_queue(queue):
    return queue

class MP_Handler():
    def make_server_manager(self, ipaddr, port, authkey):
        """
        Creates a server manager that will manage all of the jobs in
        the job_queue that clients will pull from.
        """

        # TODO: Probably need to make these multiprocessing queues?
        # Getting an NotImplementedException on OSX when using them though
        # and trying to call qsize()... Oh well, its working so far...
        job_queue = Queue()
        result_queue = Queue()

        JobQueueManager.register('get_job_queue', callable=partial(get_queue, 
                                                                   job_queue))
        JobQueueManager.register('get_result_queue',
                                 callable=partial(get_queue, result_queue))

        manager = JobQueueManager(address=(ipaddr, port), authkey=authkey)
        manager.start()
        logging.debug("Multiprocessing Server Started: %s:%s" % (ipaddr, port))
        return manager

    def word_count(self, textblob, regex):
        words = re.findall(regex, textblob.lower())
        return Counter(words)

    def counter_worker(self, job_queue, result_queue):
        process = multiprocessing.current_process()
        logging.debug("%s: STARTING UP!" % process)

        while True:
            try:
                job = job_queue.get_nowait()
                logging.debug("%s: I have a job!!!" % process)

                results = self.word_count(job[0], job[1])
                result_queue.put(results)
                logging.debug("%s: Added results to the "
                              "result_queue" % process)

            except Empty:
                logging.debug("%s: No work! Returning.", process)
                return

    def mp_counter(self, shared_job_queue, shared_result_queue, nprocs):
        procs = []
        for i in range(nprocs):
            p = multiprocessing.Process(target=self.counter_worker,
                                        args=(shared_job_queue,
                                              shared_result_queue))
            logging.debug("Created process %d" % i)
            procs.append(p)

        for p in procs:
            p.start()

        for p in procs:
            p.join()

    def make_client_manager(self, ip, port, authkey):
        class ServerQueueManager(SyncManager):
            pass

        ServerQueueManager.register('get_job_queue')
        ServerQueueManager.register('get_result_queue')

        manager = ServerQueueManager(address=(ip, port), authkey=authkey)

        try:
            manager.connect()
        except Exception,e:
            logging.error("%s" % e)
            sys.exit(1)

        logging.debug("Client connected to %s:%s" % (ip, port))
        return manager
