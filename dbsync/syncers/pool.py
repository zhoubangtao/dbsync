# -*- coding:utf-8 -*-

import concurrent.futures

from base import BaseSyncer, sync_data, incr_sync_by_day


class BasePoolSyncer(BaseSyncer):
    def __init__(self, store, pool, serializer=None, notifier=None):
        super(BasePoolSyncer, self).__init__(store, serializer, notifier)
        self._pool = pool

    def sync(self):
        self._pool.submit(sync_data, self._store, self._serializer, 'data.txt')
        # sync_data(self._store, self._serializer, 'data.txt')

    def incr_sync_by_day(self):
        self._pool.submit(incr_sync_by_day, self._store, self, self._serializer)

    def stop(self):
        self._pool.shutdown()


class ThreadPoolSyncer(BasePoolSyncer):
    """
    An executor that runs jobs in a concurrent.futures thread pool.

    Plugin alias: ``threadpool``

    :param max_workers: the maximum number of spawned threads.
    """

    def __init__(self, store, serializer=None, notifier=None, max_workers=10):
        pool = concurrent.futures.ThreadPoolExecutor(int(max_workers))
        super(ThreadPoolSyncer, self).__init__(store, pool, serializer, notifier)


class ProcessPoolSyncer(BasePoolSyncer):
    """
    An executor that runs jobs in a concurrent.futures process pool.

    Plugin alias: ``processpool``

    :param max_workers: the maximum number of spawned processes.
    """

    def __init__(self, store, serializer=None, notifier=None, max_workers=10):
        pool = concurrent.futures.ProcessPoolExecutor(int(max_workers))
        super(ProcessPoolSyncer, self).__init__(store, pool, serializer, notifier)

