# -*- coding:utf-8 -*-

import pymongo
import bson
import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.url import URL


class Mysql():

    def __init__(self, username=None, password=None, host=None, port=None, database=None, query=None, table=None):
        self._engine = self._get_engine(username=username, password=password, host=host, port=port, database=database, query=query)
        self._table = table

    def get_schema(self):
        meta = MetaData()
        meta.reflect(bind=self._engine)
        table = meta.tables[self._table]

        obj = {"type": "object", "properties": {}}
        for column in table.columns:
            obj["properties"][column.name.lower()] = {}
            obj["properties"][column.name.lower()]["type"] = column.type.__visit_name__.lower()
            obj["properties"][column.name.lower()]["description"] = column.description
            obj["properties"][column.name.lower()]["required"] = not column.nullable
            obj["properties"][column.name.lower()]["default"] = column.default

        return obj

    def _get_engine(self, username=None, password=None, host=None, port=None, database=None, query=None):
        drivername = "mysql+mysqldb"
        url = URL(drivername=drivername, username=username, password=password, host=host, port=port, database=database, query=query)
        return create_engine(url)


MONGO_DATA_TYPES = {
    bson.int64.Int64: "bigint",
    int: 'int',
    bool: 'boolean',
    datetime.datetime: 'datetime',
    bson.objectid.ObjectId: 'string',
    unicode: 'string',
}

class Mongo():

    def __init__(self):
        self._collection = None

    def get_schema(self):

        schema = {"type": 'object', "properties": {}}

        rs = self._collection.find().sort("_id", pymongo.DESCENDING).limit(1000)

        for row in rs:
            for key in row:
                schema["properties"][key] = {}
                schema["properties"][key]['type'] = MONGO_DATA_TYPES[type(row[key])]
                if isinstance(row[key], list):
                    schema["properties"][key]['items'] = {}
                    if len(row[key] > 0):
                        schema["properties"][key]['items']['type'] = MONGO_DATA_TYPES[type(row[key][0])]
                    else:
                        schema["properties"][key]['items']['type'] = 'unknown'


                schema["properties"][key]['required'] = False
                schema["properties"][key]['description'] = ""
                schema["properties"][key]['default'] = None


    def format_dict(self, properties, data):
        for key in data:
            properties[key] = {}

            if isinstance(data[key], dict):
                properties[key]["type"] = MONGO_DATA_TYPES[type(data[key])]




