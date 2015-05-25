# -*- coding:utf-8 -*-

import unittest
import dbsync.utils.dt as dt

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_dt(self):
        startday, endday = dt.get_day_range()
        print startday

        starttime, endtime = dt.get_hour_range()
        print starttime
        print endtime

if __name__ == '__main__':
    unittest.main()
