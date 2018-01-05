'''
Created on 06.12.2017

@author: mabelli
'''
from Database.Basic import Basic
from Database.Tables import t_Company, t_System, t_Setting, t_Color, t_Color_Type,\
                            t_Paint_Scheme, t_Paint_Scheme_Line, zt_System_Setting
from Database.CreateDatabase import create_database as cdb
from Database.Tables import create_tables as ct

class DBService():
    
    def __init__(self):
        basic = Basic()
        self.con        = basic.con
        self.base       = basic.base
        self.meta       = basic.meta
        self.session    = basic.session
    
    def drop_tables(self):
        self.base.metadata.drop_all(self.con)
    
    def create_tables(self):
        ct(self.meta, self.con, self.session)
        
    def create_dataBase(self):
        cdb(self.session)
    
    def _get_from_DB(self, tabletype):  
        ret = []      
        for table in self.session.query(tabletype).order_by(tabletype.ID):
            ret.append(table)
        return ret
    
    def get_companies(self):
        return self._get_from_DB(t_Company)
        
    def get_systems(self):
        return self._get_from_DB(t_System)
    
    def get_settings(self):
        return self._get_from_DB(t_Setting)
    
    def get_color(self):
        return self._get_from_DB(t_Color)
    
    def get_full_colors(self):
        ret = []
        for table in self.session.query(t_Color.Name,
                                        t_Company.Name.label("Company name"),
                                        t_Color_Type.Name.label("Color type"),
                                        t_Color.InStock, 
                                        t_Color.Owned).join(t_Company).join(t_Color_Type).filter(
                                            t_Company.ID == t_Color.C_ID,
                                            t_Color_Type.ID == t_Color.CT_ID):
            ret.append(table)
        return ret
            
    
    def get_color_type(self):
        return self._get_from_DB(t_Color_Type)
    
    def get_paint_scheme(self):
        return self._get_from_DB(t_Paint_Scheme)
    
    def get_paint_scheme_line(self):
        return self._get_from_DB(t_Paint_Scheme_Line)
    
    def get_zt_system_setting(self):
        return self._get_from_DB(zt_System_Setting)            