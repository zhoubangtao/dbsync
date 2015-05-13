__author__ = 'nathan'

import unittest
import pytest
import sqlite3
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
import json
import collections

try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock, MagicMock


class MyTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        metadata = MetaData()
        users = Table('users', metadata,
            Column('ID', Integer, primary_key=True),
            Column('name', String),
            Column('fullname', String),
        )
        metadata.create_all(engine)

        ins = users.insert().values(name='jack', fullname='Jack Jones')
        self.conn = engine.connect()
        result = self.conn.execute(ins)

    def test_sqlachemy(self):
        # self.assertEqual(True, False)
        users = self.conn.execute("select * from users")
        print users.__module__
        print dir(users)
        for row in users:
            print dir(row)
            print row.keys()
            print json.dumps(collections.OrderedDict((key.lower(), row[key]) for key in row.keys()))

        # print json.dumps(dict(users.first().items()))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
