import logging
import time
import re
import Queue
import multiprocessing
from multiprocessing.managers import SyncManager
from collections import Counter

class MP_Handler():
    def make_server_manager(self, ipaddr, port, authkey):
        # TODO: Probably need to make these multiprocessing queues?
        # Getting an NotImplementedException on OSX when using them though
        # and trying to call qsize()... Oh well, its working so far...
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()

        class JobQueueManager(SyncManager):
            pass

        JobQueueManager.register('get_job_queue', callable=lambda: job_queue)
        JobQueueManager.register('get_result_queue',
                                 callable=lambda: result_queue)

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
                logging.debug("%s: Added results to the result_queue" % process)

            except Queue.Empty:
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

        manager = ServerQueueManager(address=(ip,port), authkey=authkey)
        manager.connect()

        logging.debug("Client connected to %s:%s" % (ip, port))
        return manager
