# -*- coding:utf-8 -*-
__author__ = 'nathan'
import six

from abc import ABCMeta, abstractmethod

class BaseNotifier(six.with_metaclass(ABCMeta, object)):
    """Abstract base class that defines the interface that every serializer must implement."""

    def notify(self):
        self._notify()

    @abstractmethod
    def _notify(self):
        pass