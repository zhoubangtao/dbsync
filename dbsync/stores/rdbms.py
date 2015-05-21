# -*- coding:utf-8 -*-
__author__ = 'nathan'

import collections

from .base import BaseStore
from sqlalchemy.sql import text, select, and_
from sqlalchemy import MetaData

class DatabaseStore(BaseStore):
    """
        It stands for a table or a sql result
    """

    def __init__(self, engine, schema, table, columns=None, where=None, split_by=None):
        """
        create a new DatabaseStore, which stand for a table from a rdbms

        Parameters:
          - `engine`: the sqlalchemy engine instance
          - `schema`: database schema
          - `table`: the table that needs to be synced
          _ `columns`: the column that needs to be synced, it should be str(one column),
          comma split str(multi columns) or a list of str
          - `where`: a where clouse, only the condition
          - `split_by`: when sync the table concurrently, which cloumn should it be splitted by

        """
        self.__engine = engine
        self.__conn = engine.connect()
        self.__schema = schema
        self.__table = table
        self.__splits = None
        self.__columns = columns
        self.__where = where
        self.__split_by = split_by if split_by is not None else self.__get_split_by()


    def sql(self):
        str(self.__select())

    def __format_columns(self, columns):
        """

        :param columns:
        :return:
        """
        if isinstance(columns, str):
            return columns
        else:
            return ",".join(self.__columns) if self.__columns is not None and len(self.__columns) > 0 else "*"

    def __select(self):
        where = '' if self.__where is None else self.__where

        select(text(self.__format_columns(self.__columns))).\
            where(text(where)).\
            select_from(text(self.__table))


    def __select_with_split_by(self, start, end):
        where = '' if self.__where is None else self.__where

        select(text(self.__format_columns(self.__columns))).\
            where(
                and_(
                    text(where),
                    text(":split_by between :start and :end"))
                ).\
            select_from(text(self.__table)).params(split_by=self.__split_by, start=start, end=end)


    def count(self):
        self.__select().count()

    def __iter__(self):
        return self

    def __next__(self):
        pass

    next = __next__

    def get_split(self):
        pass

    def get(self, partition):
        result = self.__conn.execute(partition)
        for row in result:
            yield collections.OrderedDict((key.lower(), row[key]) for key in row.keys())

    def put(self, iterable):
        for row in iterable:
            # TODO: the data show be insert into database
            self.__engine.insert(row)

    def get_local(self, local_path, merge=False):
        pass

    def __get_split_by(self):
        meta = MetaData()
        meta.reflect(bind=self.__engine)
        _table = meta.tables[self.__table]

        primary_keys = _table.primary_key.columns
        if len(primary_keys) == 1:
            return primary_keys.keys()[0].lower()
        else:
            return None

    def split(self, split_nums=1):
        """
        :return: should return a partition
        if split_nums = 1, means no need to split, return the whole sql
        if
        """
        where = '' if self.__where is None else self.__where

        if split_nums > 1:
            record_nums_per_split = self.count()/split_nums

            select(text(self.__format_columns(self.__columns))).\
            where(
                and_(
                    text(where),
                    text()
                )
            ).\
            order_by(self.__split_by).\
            select_from(text(self.__table))

            #select * from users where split_by > 100 limit 200

        else:
            self.sql()

