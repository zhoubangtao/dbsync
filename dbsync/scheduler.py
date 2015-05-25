# -*- coding:utf-8 -*-
import pytz

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import time

jobstores = {
    # 'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    'default': MemoryJobStore()
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,
                                job_defaults=job_defaults, timezone=pytz.timezone('Asia/Shanghai'))

def say_hello(name):
    print "Hello " + name

def sync(store, syncer):
    syncer.sync(store)

def incr_sync_by_hour(store, syncer):
    syncer.sync_by_hour(store)

def incr_sync_by_day(store, syncer):
    syncer.sync_by_day(store)


scheduler.add_job()

scheduler.add_job(say_hello, 'interval', ["Bangtao"], seconds=2)
scheduler.add_job(say_hello, 'interval', ["Baixue"], seconds=2)
scheduler.start()
print scheduler.get_jobs()
scheduler.print_jobs()


while True:
    time.sleep(5)

