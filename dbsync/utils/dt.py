# -*- coding:utf-8 -*-
import datetime

def get_day_range(now=None):

    now = datetime.date.today() if now is None else now

    delta = now - datetime.timedelta(days=1)
    starttime = datetime.datetime.combine(delta, datetime.time())
    endtime = datetime.datetime.combine(now, datetime.time())

    return starttime, endtime


def get_hour_range(now=None):
    now = datetime.datetime.now() if now is None else now
    now = now.replace(minute=0, second=0, microsecond=0)

    delta = now - datetime.timedelta(hours=1)
    return delta, now

