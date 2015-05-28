# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import pymongo
import os
import json
import settings

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from dbsync.models import DataSource, Job, History
from sqlalchemy.orm import sessionmaker

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class JobIndexHandler(tornado.web.RequestHandler):
    def get(self):
        # jobs = self.application.db.query(Job)
        source = DataSource(id=1, type='MySQL', instance='main', host='localhost', port=3306, username='root', passwd='root')
        job1 = Job(id=1, database='test', database_eval=False, table='test', table_eval=False, sync_type='overwrite', datasource=source)
        job1.status = 'Run'
        job2 = Job(id=2, database='test', database_eval=False, table='("user"+str(x) if x>0 else "user" for x in range(0,2))', table_name='user', table_eval=True, sync_type='overwrite', datasource=source)
        job2.status = 't'
        jobs = (job1, job2)
        self.render('jobs/index.html', jobs=jobs, active="jobs")

class JobShowHandler(tornado.web.RequestHandler):
    def get(self, id):
        job = self.application.db.query(Job).filter(Job.id == id).first()
        self.render('jobs/show.html', job=job, active="jobs")

class JobNewHandler(tornado.web.RequestHandler):
    def get(self):
        datasources = self.application.db.query(DataSource)
        self.render('jobs/new.html', datasources=datasources, active="jobs")

    def post(self):
        pass

        self.redirect('jobs')


class DataSourceIndexHandler(tornado.web.RequestHandler):

    def get(self):
        datasources = self.application.db.query(DataSource)
        self.render('datasources/index.html', datasources=datasources, active="datasources")


class DataSourceShowHandler(tornado.web.RequestHandler):

    def get(self, id):
        datasource = self.application.db.query(DataSource).filter(DataSource.id == id).first()
        self.render('datasources/show.html', datasource=datasource, active="datasources")

class DataSourceNewHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('datasources/new.html', active="datasources")

    def post(self):
        type = self.get_argument('type', 'MySQL')
        instance = self.get_argument('instance', 'main')
        host = self.get_argument('host', 'localhost')
        port = self.get_argument('port', 3306)
        username = self.get_argument('username')
        passwd = self.get_argument('passwd')
        query = self.get_argument('query', '')

        source = DataSource(type=type, instance=instance, host=host, port=port, username=username, passwd=passwd, query=query)

        db = self.application.db

        db.add(source)
        db.commit()

        self.redirect('/datasources')

class DataSourceEditHandler(tornado.web.RequestHandler):

    def get(self, id):
        datasource = self.application.db.query(DataSource).filter(DataSource.id == id).first()
        self.render('datasources/edit.html', datasource=datasource, active="datasources")

    def post(self, id):
        type = self.get_argument('type', 'MySQL')
        instance = self.get_argument('instance', 'main')
        host = self.get_argument('host', 'localhost')
        port = self.get_argument('port', 3306)
        username = self.get_argument('username')
        passwd = self.get_argument('passwd')
        query = self.get_argument('query', '')

        db = self.application.db
        db.query(DataSource).filter(DataSource.id == id).update({'type': type, 'instance': instance, 'host': host, 'port': port, 'username': username, 'passwd': passwd, 'query': query})
        db.commit()

        self.redirect('/datasources')

class DataSourceDeleteHandler(tornado.web.RequestHandler):

    def post(self, id):

        db = self.application.db
        db.query(DataSource).filter(DataSource.id == id).delete()
        db.commit()
        self.redirect('/datasources')

    get = post


class DataSourceGetDatabasesHandler(tornado.web.RequestHandler):
    def get(self, id):
        datasource = self.application.db.query(DataSource).filter(DataSource.id == id).first()
        databases = list()
        if datasource.type.lower() == 'mysql':

            url = URL(drivername=settings.MYSQL_DRIVER_NAME, username=datasource.username,
                      password=datasource.passwd, host=datasource.host, port=datasource.port, database='test')

            engine = create_engine(url)
            rs = engine.execute('show databases')
            for row in rs:
                database = row[0]
                if database not in ("information_schema", "mysql", "performance_schema"):
                    databases.append(database)
        else:
            client = pymongo.MongoClient(host=datasource.host, port=datasource.port)
            databases = client.database_names()


        self.write({'data': databases})

class DataSourceGetTablesHandler(tornado.web.RequestHandler):
    def get(self, id, database):

        datasource = self.application.db.query(DataSource).filter(DataSource.id == id).first()
        tables = list()
        if datasource.type.lower() == 'mysql':
            url = URL(drivername=settings.MYSQL_DRIVER_NAME, username=datasource.username,
                      password=datasource.passwd, host=datasource.host, port=datasource.port    , database='test')

            engine = create_engine(url)
            rs = self.application.engine.execute('select TABLE_NAME from INFORMATION_SCHEMA.TABLES '
                                             'where TABLE_SCHEMA="%s";' % database)
            for row in rs:
                tables.append(row[0])
        else:
            client = pymongo.MongoClient(host=datasource.host, port=datasource.port)
            tables = client[database].collection_names()
        self.write({'data': tables})

class HistoryIndexHandler(tornado.web.RequestHandler):
    def get(self):
        histories = self.application.db.query(History)
        self.render('history/index.html', active='history')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/datasources", DataSourceIndexHandler),
            (r"/datasources/new", DataSourceNewHandler),
            (r"/datasources/(\d+)/show", DataSourceShowHandler),
            (r"/datasources/(\d+)/edit", DataSourceEditHandler),
            (r"/datasources/(\d+)/delete", DataSourceDeleteHandler),
            (r"/datasources/(\d+)/database", DataSourceGetDatabasesHandler),
            (r"/datasources/(\d+)/database/(\w+)", DataSourceGetTablesHandler),
            (r"/jobs", JobIndexHandler),
            (r"/jobs/new", JobNewHandler),
            (r"/jobs/(\d+)/show", JobShowHandler),
            (r"/history", HistoryIndexHandler),
        ]
        settings = dict(
            template_path = TEMPLATE_PATH,
            static_path = STATIC_PATH,
            debug = True
        )

        tornado.web.Application.__init__(self, handlers, **settings)
        self.engine = create_engine("mysql://root:root@localhost/test")
        Session = sessionmaker(bind=self.engine)

        self.db = Session()



if __name__ == "__main__":
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()