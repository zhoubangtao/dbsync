# -*- coding:utf-8 -*-
__author__ = 'nathan'

import threading
import logging
import time
import codecs
import six

from abc import ABCMeta, abstractmethod

class BaseSyncer(six.with_metaclass(ABCMeta, object)):
    """Abstract base class that defines the interface that every syncer must implement."""

    _logger = logging.getLogger("dbsync.syncers")

    @abstractmethod
    def __init__(self, serializer, model, notifier):
        super(BaseSyncer, self).__init__()
        self.serializer = serializer
        self.model = model
        self.notifier = notifier

    def setup(self):
        pass

    def merge(self):
        pass

    def target(self):
        pass

    @abstractmethod
    def sync(self):
        pass

    @abstractmethod
    def incr_sync(self, fields):
        """

        :param fields:
        :return:
        """
        pass

    def cleanup(self):
        pass

