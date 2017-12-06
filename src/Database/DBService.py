'''
Created on 06.12.2017

@author: mabelli
'''
from Database.Basic import Basic
from Database.Tables import t_System
from Database.CreateDatabase import createDatabase as cdb
from Database.Tables import createTables as ct

class DBService():
    
    def __init__(self):
        basic = Basic()
        self.con        = basic.con
        self.base       = basic.base
        self.meta       = basic.meta
        self.session    = basic.session
    
    def createTables(self):
        ct(self.meta, self.con, self.session)
        
    def createDataBase(self):
        cdb(self.session)
    
    def getSystems(self):
        ret = []
        for system in self.session.query(t_System).order_by(t_System.ID):
            ret.append(system)
        return ret
            