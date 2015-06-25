import logging
from collections import Counter

class MP_Handler():
    self.logger = logging.getLogger(__name__)
    
    def popular_words(self, file, amt_of_words, regex):
        words = re.findall(regex, file.read().lower())
        return Counter(words).most_common(amt_of_words)

    def counter_worker(self, job_queue, result_queue):
        while True:
            try:
                job = job_q.get_nowait()
                outdict = {x[0]: self.popular_words(x[0], x[1], x[2])
                                                 for x in job}
                result_q.put(outdict)
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

    def make_server_manager(ipaddr, port, authkey):
        job_queue = Queue.Queue()
        result_queue = Queue.Queue()

        class JobQueueManager(SyncManager):
            pass

        JobQueueManager.register('get_job_queue', callable=lambda: job_queue)
        JobQueueManager.register('get_result_queue',
                                 callable=lambda: result_queue)

        manager = JobQueueManager(address=(ipaddr, port), authkey=authkey)
        manager.start()
        logger.debug("Multiprocessing Server Started: %s:%s" % (ipaddr, port))
        return manager

    def runserver(self, args):
        manager = make_server_manager(args.iapddr, args.port, args.authkey)
        shared_job_queue = manager.get_job_queue()

        for file in args.files:
            shared_job_queue.put([file, args.count, args.regex])

        numresults = 0
        resultdict = {}
        while numresults < len(files):
            outdict = shared_result_queue.get()
            resultdict.update(outdict)
            numresults += len(outdict)

        time.sleep(2)
        manager.shutdown()
