# -*- coding:utf-8 -*-
__author__ = 'nathan'

import abc
import six


class BaseStore(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self):
        super(BaseStore, self).__init__()

    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def put(self):
        pass

    @abc.abstractmethod
    def exit(self):
        pass