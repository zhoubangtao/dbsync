# -*- coding:utf-8 -*-

import concurrent.futures

from base import BaseSyncer, sync_data


class BasePoolSyncer(BaseSyncer):
    def __init__(self, from_, to_, pool, serializer=None, notifier=None):
        super(BasePoolSyncer, self).__init__(from_, to_, serializer, notifier)
        self._pool = pool

    def merge(self):
        pass

    def sync(self):
        self._pool.submit(sync_data, self._from, self._to, self._serializer)

    def incr_sync(self, fields):
        self._pool.submit(sync_data)

    def stop(self):
        self._pool.shutdown()


class ThreadPoolSyncer(BasePoolSyncer):
    """
    An executor that runs jobs in a concurrent.futures thread pool.

    Plugin alias: ``threadpool``

    :param max_workers: the maximum number of spawned threads.
    """

    def __init__(self, from_, to_, serializer=None, notifier=None, max_workers=10):
        pool = concurrent.futures.ThreadPoolExecutor(int(max_workers))
        super(ThreadPoolSyncer, self).__init__(from_, to_, pool, serializer, notifier)


class ProcessPoolSyncer(BasePoolSyncer):
    """
    An executor that runs jobs in a concurrent.futures process pool.

    Plugin alias: ``processpool``

    :param max_workers: the maximum number of spawned processes.
    """

    def __init__(self, from_, to_, serializer=None, notifier=None, max_workers=10):
        pool = concurrent.futures.ProcessPoolExecutor(int(max_workers))
        super(ProcessPoolSyncer, self).__init__(from_, to_, pool, serializer, notifier)

