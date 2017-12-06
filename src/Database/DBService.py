'''
Created on 06.12.2017

@author: mabelli
'''
from Database.Basic import Basic
from Database.Tables import t_Company, t_System, t_Setting, t_Color, t_Color_Type, \
                            t_Paint_Scheme, t_Paint_Scheme_Line, zt_System_Setting, \
                            zt_Color_Color_Type
from Database.CreateDatabase import createDatabase as cdb
from Database.Tables import createTables as ct

class DBService():
    
    def __init__(self):
        basic = Basic()
        self.con        = basic.con
        self.base       = basic.base
        self.meta       = basic.meta
        self.session    = basic.session
    
    def dropTables(self):
        self.base.metadata.drop_all(self.con)
    
    def createTables(self):
        ct(self.meta, self.con, self.session)
        
    def createDataBase(self):
        cdb(self.session)
    
    def _getFromDB(self, tabletype):
        ret = []
        for table in self.session.query(tabletype).order_by(tabletype.ID):
            ret.append(table)
        return ret
    
    def getCompanies(self):
        return self._getFromDB(t_Company)
        
    def getSystems(self):
        return self._getFromDB(t_System)
    
    def getSettings(self):
        return self._getFromDB(t_Setting)
    
    def getColor(self):
        return self._getFromDB(t_Color)
    
    def getColorType(self):
        return self._getFromDB(t_Color_Type)
    
    def getPaintScheme(self):
        return self._getFromDB(t_Paint_Scheme)
    
    def getPaintSchemeLine(self):
        return self._getFromDB(t_Paint_Scheme_Line)
    
    def getZtSystemSetting(self):
        return self._getFromDB(zt_System_Setting)
    
    def getZtColorColorType(self):
        return self._getFromDB(zt_Color_Color_Type)
            