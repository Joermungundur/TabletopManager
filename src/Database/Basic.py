'''
Created on 06.12.2017

@author: mabelli
'''
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import sessionmaker
from Database.Constants import *
from sqlalchemy.schema import DDLElement
from sqlalchemy.ext import compiler
from sqlalchemy.sql import table


def __connect(user, password, db, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    con = create_engine(url, client_encoding='utf8', echo=True)

    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


class Basic:
    base = declarative_base()

    __url = 'postgresql://{}:{}@{}:{}/{}'
    __url = __url.format(dbUserName, dbPassword, dbHost, dbPort, dbName)

    con = create_engine(__url, client_encoding='utf8')

    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    __Session = sessionmaker(con)
    session = __Session()
