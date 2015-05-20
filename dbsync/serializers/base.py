# -*- coding:utf-8 -*-
__author__ = 'nathan'
import six

from abc import ABCMeta, abstractmethod


class BaseSerializer(six.with_metaclass(ABCMeta, object)):
    """Abstract base class that defines the interface that every serializer must implement."""

    def __init__(self):
        pass

    @abstractmethod
    def serialize(self, datum, *args, **kwargs):
        """
        Args:
            datum(map): one record or line data
        """
        pass
