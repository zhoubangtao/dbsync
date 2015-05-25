# -*- coding:utf-8 -*-

import abc
import six


class BaseStore(six.with_metaclass(abc.ABCMeta, object)):
    """Abstract base class that defines the interface that every store must implement."""

    def __init__(self):
        super(BaseStore, self).__init__()

    def __iter__(self):
        return self

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def incr_by_day(self):
        pass
