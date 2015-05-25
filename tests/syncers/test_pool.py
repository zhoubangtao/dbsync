# -*- coding:utf-8 -*-

import unittest
import time

from dbsync.syncers.pool import ThreadPoolSyncer, ProcessPoolSyncer
from tests.stores.test_rdbms import get_sample_data
from dbsync.stores.rdbms import DatabaseStore

class PoolSyncerTestCase(unittest.TestCase):

    def setUp(self):
        self._full_table = DatabaseStore(get_sample_data(), "users")

    def test_threadpool(self):
        ThreadPoolSyncer(self._full_table).sync()
        # ProcessPoolSyncer(self._full_table).sync()

if __name__ == '__main__':
    unittest.main()
