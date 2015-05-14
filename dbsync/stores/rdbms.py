# -*- coding:utf-8 -*-
__author__ = 'nathan'

from .base import BaseStore


class DatabaseStore(BaseStore):
    """
    as source, it can stand for a database or set of tables with or just a table
    as target, it can only stand for a table
    """

    def __init__(self, engine):
        self._engine = engine

    def put(self):
        pass

    def get(self):
        pass

    def split(self, split_by, num_splits):
        self._engine