# -*- coding:utf-8 -*-

import collections


from sqlalchemy import create_engine, select, MetaData, text, and_, or_
from sqlalchemy.engine.url import URL
from .base import BaseStore
from ..utils.dt import get_day_range, get_hour_range

class MysqlStore(BaseStore):

    def __init__(self, datasource, database, table, create_column=None, update_column=None):
        super(MysqlStore, self).__init__(datasource, database, table,
                                         create_column=create_column,
                                         update_column=update_column)

        self._engine = self._get_engine(username=datasource.username,
                                        password=datasource.passwd,
                                        host=datasource.host,
                                        port=datasource.port,
                                        database=database,
                                        query=datasource.query)

    def all(self):
        connection = self._engine.connect()
        result = connection.execute(select([text("*")]).select_from(self._table))
        print result
        for row in result:
            yield collections.OrderedDict((key.lower(), row[key]) for key in row.keys())

    def incr_by_day(self):
        starttime, endtime = get_day_range()
        create_column, update_column = self._get_default_create_and_update_column()

        res = self._engine.execute(
            self._select_incr(create_column=create_column, create_start_time=str(starttime),
                              create_end_time=str(endtime), update_column=update_column,
                              update_start_time=str(starttime), update_end_time=str(endtime)))

        for record in res:
            yield record

    def incr_by_hour(self):
        pass

    def _select_incr(self, table, create_column, create_start_time, create_end_time, update_column, update_start_time, update_end_time):
        sel = select([text("*")]).where(
            or_(text("%s between '%s' and '%s'" % (create_column, create_start_time, create_end_time)),
                 text("%s between '%s' and '%s'" % (update_column, update_start_time, update_end_time)))
        ).select_from(text(table))
        return sel

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
        meta.reflect(bind=self._engine)
        table = meta.tables[self._table]

        keys = table.columns.keys()
        return (key.lower() for key in keys)

    def _get_engine(self, username=None, password=None, host=None, port=None, database=None, query=None):
        drivername = "mysql+mysqldb"
        url = URL(drivername=drivername, username=username, password=password, host=host, port=port, database=database, query=query)
        return create_engine(url)