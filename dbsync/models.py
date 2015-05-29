# -*- coding:utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataSource(Base):

    __tablename__ = 'datasource'

    id = Column(Integer, primary_key=True)
    type = Column(String(255))
    instance = Column(String(255))
    host = Column(String(255))
    port = Column(Integer)
    username = Column(String(255))
    passwd = Column(String(255))
    query = Column(String(255))
    disabled = Column(Boolean)
    create_at = Column(DateTime)
    update_at = Column(DateTime)
    jobs = relationship('Job', backref="datasource")

class Job(Base):

    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    datasource_id = Column(Integer, ForeignKey('datasource.id'))
    database = Column(String(255))
    database_eval = Column(Boolean)
    database_name = Column(String(255))
    table = Column(String(255))
    table_eval = Column(Boolean)
    table_name = Column(String(255))
    create_column = Column(String(255))
    update_column = Column(String(255))
    json_schema = Column(Text)
    sync_type = Column(String(25)) # overwrite:全表覆盖，inc_by_table:全表天分区，inc_by_datatime:按时间戳的增量分t区



class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)


