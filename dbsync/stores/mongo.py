# -*- coding:utf-8 -*-
__author__ = 'nathan'

import pymongo

from .base import BaseStore
from ..utils.dt import get_day_range


class MongoStore(BaseStore):
    """
        It stands for a table or a sql result, split to some javascript snippets
    """

    def __init__(self, datasource, database, collection, create_column=None, update_column=None):
        super(MongoStore, self).__init__(datasource, database, collection,
                                         create_column=create_column,
                                         update_column=update_column)

        client = pymongo.MongoClient(host=datasource.host, port=datasource.port)
        self._collection = client[database][collection]

    def __iter__(self):
        return self

    def __next__(self):
        for record in self._collection.find():
            yield record

    next = __next__

    def all(self):
        # client = pymongo.MongoClient(hostname, port, tz_aware=True)

        # res = client[database][collection].find()
        res = self._collection.find()

        for record in res:
            yield record

    def incr_by_hour(self):
        pass

    def incr_by_day(self):
        starttime, endtime = get_day_range()
        res = self._collection.find({'$or': {'create_time': {'$gte': starttime, '$lte': endtime},
                                       'update_time': {'$gte': starttime, '$lte': endtime}}})

        for record in res:
            yield record
