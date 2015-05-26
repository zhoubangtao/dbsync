# -*- coding:utf-8 -*-

import collections


from sqlalchemy import select, MetaData, text, and_, or_
from .base import BaseStore
from ..utils.dt import get_day_range, get_hour_range

class MysqlStore(BaseStore):

    def __init__(self, database, table, create_column=None, update_column=None, database_eval=False, table_eval=False):
        super(MysqlStore, self).__init__(database, table, database_eval, table_eval)
        self.create_column = create_column
        self.update_column = update_column

    def all(self):
        connection = self.__engine.connect()
        result = connection.execute(select().select_from(self.__table))
        for row in result:
            yield collections.OrderedDict((key.lower(), row[key]) for key in row.keys())

    def incr_by_day(self):
        starttime, endtime = get_day_range()
        create_column, update_column = self._get_default_create_and_update_column()

        res = self.__engine.execute(
            self._select_incr(create_column=create_column, create_start_time=str(starttime),
                              create_end_time=str(endtime), update_column=update_column,
                              update_start_time=str(starttime), update_end_time=str(endtime)))

        for record in res:
            yield record

    def incr_by_hour(self):
        pass

    def _select_incr(self,create_column, create_start_time, create_end_time, update_column, update_start_time, update_end_time):
        sel = select([text("*")]).where(
            or_(text("%s between '%s' and '%s'" % (create_column, create_start_time, create_end_time)),
                 text("%s between '%s' and '%s'" % (update_column, update_start_time, update_end_time)))
        ).select_from(text(self.__table))

    def _get_default_create_and_update_column(self):
        columns = self._get_columns()

        if self.create_column is not None and self.update_column is not None:
            return self.create_column, self.update_column

        if 'createtime' in columns:
            return 'createtime', 'updatetime'
        else:
            return 'create_datetime', 'update_datetime'

    def _get_columns(self):
        meta = MetaData()
        meta.reflect(bind=self.__engine)
        _table = meta.tables[self.__table]

        keys = _table.columns.keys()
        return (key.lower() for key in keys)