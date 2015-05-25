__author__ = 'nathan'

import unittest
import pytest
import sqlite3
import json
import collections
import pymongo
import MySQLdb

from MySQLdb.cursors import SSCursor
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

try:
    from unittest.mock import Mock, MagicMock
except ImportError:
    from mock import Mock, MagicMock

def convert_bit(b):

    #b = "\x00" * (8 - len(b)) + "\x01" # pad w/ zeroes
    #return struct.unpack(">Q", b)[0]
    b = '\x01' == b
    return b

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import BINARY
from sqlalchemy.dialects.mysql import BIT

@compiles(BIT, "mysql")
def compile_binary_mysql(type_, compiler, **kw):
    return "BOOLEAN"

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # orig_conv = pymysql.converters.conversions
        # orig_conv = MySQLdb.converters.conversions
        #Adding support for bit data type
        # orig_conv[MySQLdb.converters.FIELD_TYPE.BIT] = convert_bit
        # self.engine = create_engine('sqlite:///:memory:', echo=True, connect_args=dict({'autocommit': False, 'cursorclass': SSCursor, 'conv': orig_conv}))
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        metadata = MetaData()
        users = Table('users', metadata,
            Column('ID', Integer, primary_key=True),
            Column('name', String),
            Column('fullname', String),
        )
        metadata.create_all(self.engine)

        ins = users.insert().values(name='jack', fullname='Jack Jones')
        self.conn = self.engine.connect()
        result = self.conn.execute(ins)

    def test_sqlachemy(self):
        # self.assertEqual(True, False)
        users = self.conn.execute("select * from users")
        print users.__module__
        print dir(users)
        for row in users:
            print json.dumps(collections.OrderedDict((key.lower(), row[key]) for key in row.keys()))

        # print json.dumps(dict(users.first().items()))

    def test_reflection(self):
        meta = MetaData()
        meta.reflect(bind=self.engine)
        users_table = meta.tables['users']

        print "user_table:", users_table.primary_key.columns.keys()[0]

        print users_table.columns.keys()

    def test_pymongo(self):
        client = pymongo.MongoClient('localhost', 2107)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
