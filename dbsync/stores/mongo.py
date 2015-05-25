# -*- coding:utf-8 -*-
__author__ = 'nathan'

import pymongo

from .base import BaseStore
from ..utils.dt import get_day_range


class MongoStore(BaseStore):
    """
        It stands for a table or a sql result, split to some javascript snippets
    """

    def __init__(self, client, database, collection):
        self._coll = client[database][collection]

    def __iter__(self):
        return self

    def __next__(self):
        for record in self._coll.find():
            yield record

    next = __next__

    def all(self):
        # client = pymongo.MongoClient(hostname, port, tz_aware=True)

        # res = client[database][collection].find()
        res = self._coll.find()

        for record in res:
            yield record

    def incr_by_hour(self):
        pass

    def incr_by_day(self):
        starttime, endtime = get_day_range()
        res = self._coll.find({'$or': {'create_time': {'$gte': starttime, '$lte': endtime},
                                       'update_time': {'$gte': starttime, '$lte': endtime}}})

        for record in res:
            yield record
