import logging
import re
import Queue
import multiprocessing
from multiprocessing.managers import SyncManager
from collections import Counter

class MP_Handler():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
    
    def runserver(self, ipaddr, port, authkey, files, count, regex):
        manager = self.make_server_manager(ipaddr, port, authkey)
        shared_job_queue = manager.get_job_queue()

        for file in files:
            shared_job_queue.put([file, count, regex])

        numresults = 0
        resultdict = {}
        while numresults < len(files):
            outdict = shared_result_queue.get()
            resultdict.update(outdict)
            numresults += len(outdict)

        time.sleep(2)
        logging.debug("Multiprocessing Server Manager is shutting down...")
        manager.shutdown()
        logging.debug("Multiprocessing Server Manager has shut down.")

    def make_server_manager(self, ipaddr, port, authkey):
        job_queue = Queue()
        result_queue = Queue()

        class JobQueueManager(SyncManager):
            pass

        JobQueueManager.register('get_job_queue', callable=lambda: job_queue)
        JobQueueManager.register('get_result_queue',
                                 callable=lambda: result_queue)

        manager = JobQueueManager(address=(ipaddr, port), authkey=authkey)
        manager.start()
        logging.debug("Multiprocessing Server Started: %s:%s" % (ipaddr, port))
        return manager

    def popular_words(self, file, amt_of_words, regex):
        words = re.findall(regex, file.read().lower())
        return Counter(words).most_common(amt_of_words)

    def counter_worker(self, job_queue, result_queue):
        while True:
            try:
                job = job_queue.get_nowait()
                results = self.popular_words(job[0], job[1], job[2])
                outdict = {job[0]: results}

                logging.debug("Counter_Worker: Adding file \"%s\" with results "
                              "to result queue: %s" % (job[0].name, results))
                result_queue.put(outdict)
            except Queue.Empty:
                return

    def mp_counter(self, shared_job_queue, shared_result_queue, nprocs):
        procs = []
        for i in range(nprocs):
            p = multiprocessing.Process(target=self.counter_worker,
                                        args=(shared_job_queue,
                                              shared_result_queue))
            procs.append(p)
            p.start()

            for p in procs:
                p.join()
