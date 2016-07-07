import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), index=True)
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Purge(Base):
    __tablename__ = 'purges'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer)
    host_id = Column(Integer)

    purged_at = Column(DateTime, default=datetime.datetime.utcnow)

class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    hostname = Column(String(255), unique=True)
    ip = Column(String(255))

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
