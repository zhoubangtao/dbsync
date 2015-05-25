
import unittest
import json

from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
# from dbsync import DBSync
from dbsync.stores.rdbms import DatabaseStore
from dbsync.stores.local import LocalStore
from dbsync.syncers.pool import ThreadPoolSyncer
from datetime import date, datetime

class DBSyncTestCase(unittest.TestCase):

    def test_dbsync(self):
        #DBSync().serializer().syncer().validator().start()
        engine = create_engine('oracle://vbaread:vbaread@10.1.253.15:1521/orcl', echo=True)
        rdbms = DatabaseStore(engine)
        local_file = LocalStore('data')
        ThreadPoolSyncer(rdbms, local_file).sync()

    def test_dump(self):
        engine = create_engine('oracle://vbaread:vbaread@10.1.253.15:1521/orcl', echo=True)
        res = engine.connect().execute("select * from vba.student_homework_month")
        for row in res:
            yield row

        # print json.dumps(collections.OrderedDict((key.lower(), row[key]) for key in row.keys()), cls=DatetimeJSONEncoder)

class DatetimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    unittest.main()





