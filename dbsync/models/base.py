# -*- coding:utf-8 -*-
__author__ = 'nathan'

import six

from abc import ABCMeta, abstractmethod

class BaseModel(six.with_metaclass(ABCMeta, object)):
    """Abstract base class that defines the interface that every serializer must implement."""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__()

    @abstractmethod
    def partition(self, num_partitions):
        raise NotImplementedError

    @abstractmethod
    def data_size(self):
        raise NotImplementedError

    @abstractmethod
    def avg_row_size(self):
        raise NotImplementedError

    @abstractmethod
    def row_count(self):
        raise NotImplementedError

    @abstractmethod
    def data(self):
        raise NotImplementedError
