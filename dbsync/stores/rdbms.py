# -*- coding:utf-8 -*-
__author__ = 'nathan'

import collections

from .base import BaseStore
from sqlalchemy.sql import text, select, and_, or_, func
from sqlalchemy import MetaData
from ..utils.dt import get_day_range

class DatabaseStore(BaseStore):
    """
        It stands for a table or a sql result
    """

    def __init__(self, engine, table, schema=None, columns=None, where=None, split_by=None):
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
        self.__schema = schema
        self.__table = table
        self.__splits = None
        self.__columns = self._format_columns(columns)
        self.__where = self._format_where(where)
        self.__split_by = split_by if split_by is not None else self._get_split_by()

    def sql(self):
        return str(self.__select())

    def _format_columns(self, columns):
        """
        format comma split str, list or python iterable to text wrapped list

        Arguments:
          - `columns`: a list or python iterable, or comma split str
        """
        if isinstance(columns, str):
            return (text(col) for col in columns.strip().split(","))
        else:
            return (text(col) for col in columns) \
                if columns is not None and len(columns) > 0 \
                else [text("*")]

    def _format_where(self, where):
        """
            format where closure
        """
        where = "" if where is None else where
        return where

    def _select_all(self):
        """
        select all table
        """
        sel = select([text("*")]).select_from(text(self.__table))
        return sel


    def _select_incr(self,create_column, create_start_time, create_end_time, update_column, update_start_time, update_end_time):
        sel = select([text("*")]).where(
            or_(text("%s between '%s' and '%s'" % (create_column, create_start_time, create_end_time)),
                 text("%s between '%s' and '%s'" % (update_column, update_start_time, update_end_time)))
        ).select_from(text(self.__table))

        return sel

    def _select(self):
        """
        select the table with the given columns and where closure
        """
        sel = select(self.__columns).\
            where(text(self.__where)).\
            select_from(text(self.__table))
        return sel

    def _select_with_split_by(self, start, end):
        select(text(self.__columns)).\
            where(
                and_(
                    text(self.__where),
                    text(":split_by >= :start"),
                    text(":split_by < :end"),
                    )
                ).\
            select_from(text(self.__table)).params(split_by=self.__split_by, start=start, end=end)

    def _count(self):
        sel = select([func.count(text("1"))]).\
            where(text(self.__where)).\
            select_from(text(self.__table))
        return self.__engine.execute(sel).fetchone()[0]

    def count(self):
        if not hasattr(self, 'rownums'):
            self.rownums = self.__count()
        return self.rownums

    __len__ = count

    def __iter__(self):
        return self

    def __next__(self):
        result = self.__engine.execute(self._select())
        for row in result:
            yield collections.OrderedDict((key.lower(), row[key]) for key in row.keys())

    next = __next__

    def get_split(self):
        pass

    def get(self, partition=None):
        if partition is None:
            partition = self._select()
        result = self.__engine.execute(partition)
        for row in result:
            yield collections.OrderedDict((key.lower(), row[key]) for key in row.keys())

    def put(self, iterable):
        for row in iterable:
            # TODO: the data show be insert into database
            self.__engine.insert(row)

    def get_local(self, local_path, merge=False):
        pass

    def _get_split_by(self):
        meta = MetaData()
        meta.reflect(bind=self.__engine)
        _table = meta.tables[self.__table]

        primary_keys = _table.primary_key.columns
        if len(primary_keys) == 1:
            return primary_keys.keys()[0].lower()
        else:
            return None

    def _get_columns(self):
        meta = MetaData()
        meta.reflect(bind=self.__engine)
        _table = meta.tables[self.__table]

        keys = _table.columns.keys()
        return (key.lower() for key in keys)

    def _get_split_by_upper_boundary(self, rownums_per_split, low_boundary=None):
        where = "" if low_boundary is None else self.__split_by + " >= " + str(low_boundary)

        sel = select(self.__columns).\
        where(
            and_(
                text(self.__where),
                text(where)
            )
        ).\
        order_by(self.__split_by).offset(rownums_per_split).limit(1).\
        select_from(text(self.__table))

        # upper_boundary
        row = self.__engine.execute(sel).fetchone()

        if row is not None:
            lowered_row = collections.OrderedDict((key.lower(), row[key]) for key in row.keys())
            return lowered_row[self.__split_by]

    def _get_split_by_boundaries(self, split_nums):
        """
        return like [(None, 2), (2, 3), (3, None)]
        """

        low_boundary = None
        rownums_per_split = self.count()/split_nums

        boundaries = list()
        for i in range(split_nums):
            if i == split_nums - 1:
                boundaries.append((low_boundary, None))
                break

            upper_boundary = self._get_split_by_upper_boundary(rownums_per_split, low_boundary)
            boundaries.append((low_boundary, upper_boundary))
            low_boundary = upper_boundary

        return boundaries

    def split(self, split_nums=1):
        """

        Arguments:
          - `split_nums`: if split_nums = 1, means no need to split, return the whole sql
        """
        if 1 < split_nums <= self.count():
            boundaries = self._get_split_by_boundaries(split_nums)
            return boundaries
        else:
            self.sql()

    def all(self):
        connection = self.__engine.connect()
        result = connection.execute(self._select_all())
        for row in result:
            yield collections.OrderedDict((key.lower(), row[key]) for key in row.keys())

    def incr_by_day(self):
        starttime, endtime = get_day_range()
        columns = self._get_columns()

        if 'createtime' in columns:
            create_column = 'createtime'
            update_column = 'updatetime'
        else:
            create_column = 'create_datetime'
            update_column = 'update_datetime'

        res = self.__engine.execute(
            self._select_incr(create_column=create_column, create_start_time=str(starttime),
                              create_end_time=str(endtime), update_column=update_column,
                              update_start_time=str(starttime), update_end_time=str(endtime)))

        for record in res:
            yield record

    def incr_by_hour(self):
        pass
