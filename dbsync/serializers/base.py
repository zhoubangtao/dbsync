# -*- coding:utf-8 -*-
import six
import json

from abc import ABCMeta
from datetime import date, datetime
from decimal import Decimal
from bson.objectid import ObjectId


class BaseSerializer(six.with_metaclass(ABCMeta, object)):
    """Abstract base class that defines the interface that every serializer must implement."""

    def __init__(self):
        super(BaseSerializer, self).__init__()

    def serialize(self, datum, *args, **kwargs):
        """
            serialize datum to json str

        Arguments:
          - `datum`:
          - `ensure_ascii`: boolean, default True, see alse json.dumps()
          - `cls`:
        """

        _ensure_ascii = kwargs['ensure_ascii'] if kwargs.has_key("ensure_ascii") else True

        return json.dumps(datum, ensure_ascii=_ensure_ascii, cls=DatetimeJSONEncoder)


class DatetimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
