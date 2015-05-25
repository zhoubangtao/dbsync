# -*- coding:utf-8 -*-

import logging
import six
import codecs

from abc import ABCMeta, abstractmethod
from ..serializers.base import BaseSerializer


class BaseSyncer(six.with_metaclass(ABCMeta, object)):
    """Abstract base class that defines the interface that every syncer must implement."""

    _logger = logging.getLogger("dbsync.syncers")

    @abstractmethod
    def __init__(self, store, serializer=None, notifier=None):
        """

        Args:
          - `from_`: the source store
          - `to_`: the target store
          - `serializer`:
          - `notifier`:
        """
        super(BaseSyncer, self).__init__()
        self._notifier = notifier
        self._serializer = BaseSerializer() if serializer is None else serializer

        self._store = store

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def sync(self):
        """
        start to sync data

        Arguments:
          - `from_`: the source store
          - `to_`: the target store
        """
        pass

    @abstractmethod
    def incr_sync_by_day(self):
        pass

    def hive_table(self):
        pass

    def incr_hive_table(self):
        pass

    def put(self):
        pass




def sync_data(store, serailizer, local_file):
    count = 0

    _logger = logging.getLogger("dbsync.syncers")

    with codecs.open(local_file, 'w', 'utf-8') as w:
        for record in store.all():
            print record
            w.write(serailizer.serialize(record) + "\n")
            count += 1
            if (count % 10000) == 0:
                _logger.debug("dump count : %d" % count)


def incr_sync_by_day(store, serailizer, local_file):
    count = 0

    _logger = logging.getLogger("dbsync.syncers")

    with codecs.open(local_file, 'w', 'utf-8') as w:
        for record in store.incr_by_day():
            w.write(serailizer.serailize(record) + "\n")
            count += 1
            if (count % 10000) == 0:
                _logger.debug("dump count : %d" % count)
