__author__ = 'nathan'

import unittest
import sys
import os

import logging
import logging.config
from datetime import datetime
import codecs
import threading

logging.config.fileConfig("../conf/logger.conf")
logger = logging.getLogger('dbsync')

dbsync_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger.debug(dbsync_root)
sys.path.insert(0, dbsync_root)

from dbsync.mysql.homework_sitter.uct_user import *
from dbsync.mysql.homework_sitter.comm_region import *
from dbsync.mysql.homework_sitter.vox_class import *
from dbsync.mysql.homework_sitter.vox_class_student_ref import *
from dbsync.mysql.homework_sitter.vox_school import *
from dbsync.mysql.database import *

DATA_DIR = "/data/dbsync/data/"

class MyTestCase(unittest.TestCase):
    def test_dbsync(self):

        uct_user_dumper = Dumper(''.join([DATA_DIR, "uct_user.json.", datetime.now().date().isoformat()]), UctUser.select().limit(4))
        common_region_dumper = Dumper(''.join([DATA_DIR, "comm_region.json.", datetime.now().date().isoformat()]), CommRegion.select().limit(4))
        vox_class_dumper = Dumper(''.join([DATA_DIR, "vox_class.json.", datetime.now().date().isoformat()]), VoxClass.select().limit(4))
        vox_class_student_ref_dumper = Dumper(''.join([DATA_DIR, "vox_class_student_ref.json.", datetime.now().date().isoformat()]), VoxClassStudentRef.select().limit(4))
        vox_school_dumper = Dumper(''.join([DATA_DIR, "vox_school.json.", datetime.now().date().isoformat()]), vox_school.VoxSchool.select().limit(4))

        uct_user_dumper.start()
        common_region_dumper.start()
        vox_class_dumper.start()
        vox_class_student_ref_dumper.start()
        vox_school_dumper.start()

class Dumper(threading.Thread):
    def __init__(self, dst_file, sq):
        threading.Thread.__init__(self)
        self.dst_file = dst_file
        self.sq = sq

    def run(self):
        with codecs.open(self.dst_file, 'w', 'utf-8') as w :
            for item in self.sq:
                w.write(item)

    def stop(self):
            self.thread_stop = True

if __name__ == '__main__':
    unittest.main()





