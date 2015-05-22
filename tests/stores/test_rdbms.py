# -*- coding:utf-8 -*-

import unittest

from sqlalchemy import create_engine, MetaData, Table, Column,\
    Integer, String, select, text, DateTime

from datetime import datetime
from dbsync.stores.rdbms import DatabaseStore


class DatabaseStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.__engine = create_engine('sqlite:///:memory:', echo=True)
        metadata = MetaData()
        users = Table('users', metadata,
            Column('ID', Integer, primary_key=True),
            Column('name', String),
            Column('fullname', String),
            Column('create_at', DateTime),
            Column('update_at', DateTime)
        )
        metadata.create_all(self.__engine)

        ins = users.insert().values(name='jack', fullname='Jack Jones',
                                    create_at=datetime.strptime("2015-05-10 10:02:01", "%Y-%m-%d %H:%M:%S"),
                                    update_at=datetime.strptime("2015-05-10 10:02:01", "%Y-%m-%d %H:%M:%S"))
        self.__engine.connect().execute(users.insert(), [
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
        print self.__database.split(6)


if __name__ == '__main__':
    unittest.main()
