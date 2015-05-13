# -*- coding:utf-8 -*-
__author__ = 'nathan'

import threading
import logging
import time
import codecs
import concurrent.futures

from base import BaseSyncer


class BasePoolSyncer(BaseSyncer):
    def __init__(self, serializer, model, notifier, pool):
        super(BasePoolSyncer, self).__init__(serializer, model, notifier)
        self._pool = pool



class ThreadPoolSyncer(BaseSyncer):
    """
    An executor that runs jobs in a concurrent.futures thread pool.

    Plugin alias: ``threadpool``

    :param max_workers: the maximum number of spawned threads.
    """

    def __init__(self, serializer, model, notifier, max_workers=10):
        pool = concurrent.futures.ThreadPoolExecutor(int(max_workers))
        super(ThreadPoolSyncer, self).__init__(serializer, model, notifier, pool)

    def setup(self):
        pass

    def merge(self):
        pass

    def target(self):
        pass

    def sync(self):
        pass

    def incr_sync(self, fields):
        """

        :param fields:
        :return:
        """
        pass

    def cleanup(self):
        pass

class ProcessPoolSyncer(BaseSyncer):
    """
    An executor that runs jobs in a concurrent.futures process pool.

    Plugin alias: ``processpool``

    :param max_workers: the maximum number of spawned processes.
    """

    def __init__(self, serializer, model, notifier, max_workers=10):
        pool = concurrent.futures.ProcessPoolExecutor(int(max_workers))
        super(ProcessPoolSyncer, self).__init__(serializer, model, notifier, pool)


class Dumper(threading.Thread):
    def __init__(self, dst_file, sq):
        threading.Thread.__init__(self)
        self._logger = logging.getLogger("dbsync.syncers")
        self.dst_file = dst_file
        self.sq = sq

    def run(self):
        start = time.clock()
        count = 0
        self._logger.info("run start")
        with codecs.open(self.dst_file, 'w', 'utf-8') as w :
            for item in self.sq.naive().iterator():
                w.write(item.unicode_dumps() + "\n")
                count += 1

        self._logger.info("write count : %d" % count)

        end = time.clock()
        self._logger.info("%s file count %d, run time : %.03f seconds" % (self.dst_file, count, end - start))

    def stop(self):
            self.thread_stop = True