class MP_Handler_Server():
    def popular_words(self, file, amt_of_words, regex):
        words = re.findall(regex, file.read().lower())
        return Counter(words).most_common(amt_of_words)

    def counter_worker(self, job_queue, result_queue):
        while True:
            try:
                job = job_q.get_nowait()
                outdict = {x[0]: self.popular_words(x[0], x[1], x[2]
                                                 for x in job)}
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

#    def runserver(port, auth_key):
#        manager = make_server_manager(port, auth_key)
#        shared_job_queue = manager.get_job_queue
