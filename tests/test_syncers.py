__author__ = 'nathan'

import unittest

from dbsync.stores.rdbms import DatabaseStore
from dbsync.stores.local import LocalStore
from dbsync.syncers.base import sync_data
from stores.test_rdbms import get_sample_data
from dbsync.serializers.base import BaseSerializer

class SyncersTestCase(unittest.TestCase):
    def test_base(self):
        source = DatabaseStore(get_sample_data(), "users")
        target = LocalStore("data")
        sync_data(source, target, BaseSerializer())


if __name__ == '__main__':
    unittest.main()
