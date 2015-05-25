# -*- coding:utf-8 -*-
import logging
import stores

release = "0.1.1"

logging.getLogger("dbsync")


class DBSync():

    def __init__(self):
        pass

    def syncer(self, syncer):
        return self

    def validator(self, validator):
        return self

    def serializer(self, serializer):
        return self

    def notifier(self, notifier):
        return self

    def start(self):
        pass

    def stop(self):
        pass


class Engine():

    def __init__(self):
        pass
