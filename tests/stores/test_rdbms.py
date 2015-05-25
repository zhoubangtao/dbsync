# -*- coding:utf-8 -*-

import unittest
import os

from sqlalchemy import create_engine, MetaData, Table, Column,\
    Integer, String, select, text, DateTime
from sqlalchemy.pool import NullPool
from datetime import datetime
from dbsync.stores.rdbms import DatabaseStore


class DatabaseStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.__engine = get_sample_data()
        self.__database = DatabaseStore(self.__engine, "users")

    def test_something(self):
        self.assertEqual(True, False)


    def test_splits(self):
        pass


    def test_select(self):
        _where = "name = 'jack'"

        full_table = DatabaseStore(self.__engine, "users")
        self.assertEqual(full_table.sql(), "SELECT * \nFROM users")

        full_table_with_where = DatabaseStore(self.__engine, "users", where=_where)
        print full_table_with_where.sql()

        full_table_with_where_and_split_by = DatabaseStore(self.__engine, "users", where=_where)

    def test_select_split_by(self):
        full_table_with_split_by = DatabaseStore(self.__engine, "users")
        print full_table_with_split_by.__select_with_split_by("2015-05-10", "2015-05-11")

    def test_count(self):
        print self.__database.count()

    def test_split(self):
        print self.__database.split(3)

    def test_get(self):
        yestoday  = DatabaseStore(self.__engine, "users", where="create_at > '2015-05-11'")
        for row in yestoday.get():
            print row


    def test_select_incr(self):
        print self.__database._select_incr(create_column='createtime', create_start_time='2015-10-11 00:00:00',
                                     create_end_time='2015-10-12 00:00:00', update_column='updatetime',
                                     update_start_time='2015-10-11 00:00:00', update_end_time='2015-10-12 00:00:00')


def get_sample_data():
    # engine = create_engine('sqlite:///:memory:', echo=True)
    os.remove('file.db')

    engine = create_engine('sqlite:///file.db', echo=True, poolclass=NullPool)

    metadata = MetaData()
    users = Table('users', metadata,
        Column('ID', Integer, primary_key=True),
        Column('name', String),
        Column('fullname', String),
        Column('create_at', DateTime),
        Column('update_at', DateTime)
    )
    metadata.create_all(engine)

    ins = users.insert().values(name='jack', fullname='Jack Jones',
                                create_at=datetime.strptime("2015-05-10 10:02:01", "%Y-%m-%d %H:%M:%S"),
                                update_at=datetime.strptime("2015-05-10 10:02:01", "%Y-%m-%d %H:%M:%S"))
    engine.connect().execute(users.insert(), [
        {'name': 'Jack', 'fullname': 'Jack Jones',
         'create_at': datetime.strptime("2015-05-10 10:02:01", "%Y-%m-%d %H:%M:%S"),
         'update_at': datetime.strptime("2015-05-11 10:02:01", "%Y-%m-%d %H:%M:%S")},

        {'name': 'Mick', 'fullname': 'Mick M',
         'create_at': datetime.strptime("2015-05-10 10:02:01", "%Y-%m-%d %H:%M:%S"),
         'update_at': datetime.strptime("2015-05-11 11:02:01", "%Y-%m-%d %H:%M:%S")},

        {'name': 'J', 'fullname': 'Jones',
         'create_at': datetime.strptime("2015-05-11 10:02:01", "%Y-%m-%d %H:%M:%S"),
         'update_at': datetime.strptime("2015-05-12 10:02:01", "%Y-%m-%d %H:%M:%S")},

        {'name': 'Jine', 'fullname': 'Jine Jones',
         'create_at': datetime.strptime("2015-05-11 10:02:01", "%Y-%m-%d %H:%M:%S"),
         'update_at': datetime.strptime("2015-05-13 10:02:01", "%Y-%m-%d %H:%M:%S")},

        {'name': 'Ji', 'fullname': 'Ji Jones',
         'create_at': datetime.strptime("2015-05-13 10:02:01", "%Y-%m-%d %H:%M:%S"),
         'update_at': datetime.strptime("2015-05-13 10:02:01", "%Y-%m-%d %H:%M:%S")}
    ])
    return engine

if __name__ == '__main__':
    unittest.main()
