# -*- coding:utf-8 -*-
__author__ = 'nathan'

import json

from datetime import date, datetime
from decimal import Decimal
from bson.objectid import ObjectId
from dbsync.serializers.base import BaseSerializer


class JSONSerializer(BaseSerializer):
    """ serialize model to json """

    def serialize(self, datum,  *args, **kwargs):
        """

        :param datum:
        :param ensure_ascii: boolean, default True, see alse json.dumps()
        :param cls:
        :return:
        """
        return json.dumps(datum, ensure_ascii=kwargs["ensure_ascii"], cls=kwargs["ensure_ascii"])


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