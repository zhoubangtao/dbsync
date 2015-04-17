# -*- coding:utf-8 -*-
__author__ = 'nathan'


from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import time


jobstores = {
    # 'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    'default' : MemoryJobStore()
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}


    # def jobconfs(self):
    #     jcs = super(, self).jobconfs()
    #     jcs.append('mapreduce.map.memory.mb=%s' % 4096)
    #     jcs.append('mapreduce.reduce.memory.mb=%s' % 4096)
    #     return jcs

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

def say_hello(name):
    print "Hello " + name

scheduler.add_job(say_hello, 'interval', ["Bangtao"], seconds=2)
scheduler.add_job(say_hello, 'interval', ["Baixue"], seconds=2)
scheduler.start()
print scheduler.get_jobs()
scheduler.print_jobs()


while True:
    time.sleep(5)

