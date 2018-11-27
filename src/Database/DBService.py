'''
Created on 06.12.2017

@author: mabelli
'''
from Database.Basic import Basic
from Database.Tables import t_Company, t_System, t_Setting, t_Color, t_Color_Type, \
    t_Paint_Scheme, t_Paint_Scheme_Line, zt_System_Setting, t_Brush, t_Brush_Type
from Database.CreateDatabase import create_database as cdb
from Database.Tables import create_tables as ct
from sqlalchemy import func


class DBService:

    def __init__(self):
        basic = Basic()
        self.con = basic.con
        self.base = basic.base
        self.meta = basic.meta
        self.session = basic.session

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
        for table in self.session.query(
                t_Color.ID,
                t_Color.Name,
                t_Company.Name.label("Company_name"),
                t_Color_Type.Name.label("Color_type"),
                t_Color.ID_Num,
                t_Color.InStock,
                t_Color.Owned,
                t_Color.Deleted).join(t_Company).join(t_Color_Type).filter(
            t_Company.ID == t_Color.C_ID,
            t_Color_Type.ID == t_Color.CT_ID,
            t_Color.Deleted == False).order_by(t_Color.ID):
            ret.append(table)
        return ret

    def get_full_brushes(self):
        ret = []
        for table in self.session.query(
                t_Brush.ID,
                t_Brush.Name,
                t_Company.Name.label("Company_name"),
                t_Brush_Type.Name.label("Brush_type"),
                t_Brush.Owned,
                t_Brush.Deleted).join(t_Company).join(t_Brush_Type).filter(
            t_Company.ID == t_Brush.C_ID,
            t_Brush_Type.ID == t_Brush.BT_ID,
            t_Brush.Deleted == False).order_by(t_Brush.ID):
            ret.append(table)
        return ret

    def get_color_type(self):
        return self._get_from_DB(t_Color_Type)

    def get_paint_scheme(self):
        return self._get_from_DB(t_Paint_Scheme)

    def get_paint_scheme_line(self):
        return self._get_from_DB(t_Paint_Scheme_Line)

    def get_brush_type(self):
        return self._get_from_DB(t_Brush_Type)

    def get_zt_system_setting(self):
        return self._get_from_DB(zt_System_Setting)

    def get_full_paint_schemes(self):
        ret = []
        for table in self.session.query(
                t_Paint_Scheme.ID,
                t_Paint_Scheme.Name,
                t_Paint_Scheme.S_ID,
                t_System.Name.label("System_name"),
                func.count(t_Paint_Scheme_Line.PS_ID).label("Steps")).join(t_Paint_Scheme_Line).join(t_System).filter(
            t_Paint_Scheme.Deleted == False,
            t_Paint_Scheme.ID == t_Paint_Scheme_Line.PS_ID,
            t_Paint_Scheme.S_ID == t_System.ID).group_by(t_Paint_Scheme.ID).group_by(t_System.Name).order_by(t_Paint_Scheme.Name):
            ret.append(table)
        return ret
