'''
Created on 06.12.2017

@author: mabelli
'''

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String, BigInteger, Boolean
from sqlalchemy.sql.schema import ForeignKey
from Database.Basic import Basic


class t_Company(Basic.base):
    __tablename__ = "company"

    ID = Column(BigInteger, primary_key=True)
    Name = Column(String(50))
    Description = Column(String)
    Website = Column(String(100))
    Deleted = Column(Boolean, default=False)
    systems = relationship("t_System", back_populates="company", passive_deletes=True)
    colors = relationship("t_Color", back_populates="company", passive_deletes=True)
    brushes = relationship("t_Brush", back_populates="company", passive_deletes=True)

    def __repr__(self):
        return "Id = {}\nName = {}\nDescription = {}\nWebsite = {}\nDeleted{}".format(str(self.ID),
                                                                                      str(self.Name),
                                                                                      self.Description,
                                                                                      self.Website,
                                                                                      str(self.Deleted))


class t_System(Basic.base):
    __tablename__ = "system"

    ID = Column(BigInteger, primary_key=True)
    C_ID = Column(BigInteger, ForeignKey('company.ID', ondelete='CASCADE'))
    Name = Column(String(50))
    Description = Column(String)
    Deleted = Column(Boolean, default=False)
    settings = relationship("zt_System_Setting", back_populates="system")
    company = relationship("t_Company", back_populates="systems")
    paint_schemes = relationship("t_Paint_Scheme", back_populates="systems")

    def __repr__(self):
        return "Id = {}\nC_ID = {}\nName = {}\nDescription = {}\nDeleted{}".format(str(self.ID),
                                                                                   str(self.C_ID),
                                                                                   self.Name,
                                                                                   self.Description,
                                                                                   str(self.Deleted))
class t_Setting(Basic.base):
    __tablename__ = "setting"

    ID = Column(BigInteger, primary_key=True)
    Name = Column(String(50))
    Description = Column(String)
    Deleted = Column(Boolean, default=False)
    systems = relationship("zt_System_Setting", back_populates="setting")

    def __repr__(self):
        return "Id = {}\nName = {}\nDescription = {}\nDeleted{}".format(
            str(self.ID), self.Name, self.Description, str(self.Deleted))


class t_Color(Basic.base):
    __tablename__ = "color"

    ID = Column(BigInteger, primary_key=True)
    C_ID = Column(BigInteger, ForeignKey('company.ID', ondelete='CASCADE'))
    Name = Column(String(50))
    CT_ID = Column(BigInteger, ForeignKey('color_type.ID', ondelete='CASCADE'))
    ID_Num = Column(String(50))
    Owned = Column(Boolean, default=True)
    InStock = Column(Boolean, default=True)
    Deleted = Column(Boolean, default=False)
    company = relationship("t_Company", back_populates="colors")
    scheme_lines = relationship("t_Paint_Scheme_Line", back_populates="colors", passive_deletes=True)
    type = relationship("t_Color_Type", back_populates="colors")

    def __repr__(self):
        return "Id = {}\nC_ID = {}\nName = {}\nID_Num = {}\nOwned = {}\nInStock = {}\nDeleted{}".format(
            str(self.ID), str(self.C_ID), self.Name, str(self.CT_ID), str(self.ID_Num), str(self.Owned),
            str(self.InStock), str(self.Deleted))


class t_Color_Type(Basic.base):
    __tablename__ = "color_type"

    ID = Column(BigInteger, primary_key=True)
    Name = Column(String)
    Description = Column(String)
    Deleted = Column(Boolean, default=False)
    colors = relationship("t_Color", back_populates="type")

    def __repr__(self):
        return "Id = {}\nName = {}\nDeleted{}".format(str(self.ID), self.Name, str(self.Deleted))


class t_Paint_Scheme(Basic.base):
    __tablename__ = "paint_scheme"

    ID = Column(BigInteger, primary_key=True)
    Name = Column(String(100))
    A_ID = Column(BigInteger)
    S_ID = Column(BigInteger, ForeignKey('system.ID', ondelete='CASCADE'))
    Active = Column(Boolean, default=True)
    Deleted = Column(Boolean, default=False)
    lines = relationship("t_Paint_Scheme_Line", back_populates="schemes", passive_deletes=True)
    systems = relationship("t_System", back_populates="paint_schemes")

    def __repr__(self):
        return "Id = {}\nName = {}\nA_ID = {}\nDeleted{}".format(str(self.ID), self.Name, str(self.A_ID),
                                                                 str(self.S_ID), str(self.Deleted))


class t_Paint_Scheme_Line(Basic.base):
    __tablename__ = "paint_scheme_line"

    ID = Column(BigInteger, primary_key=True)
    PS_ID = Column(BigInteger, ForeignKey('paint_scheme.ID', ondelete='CASCADE'))
    Label = Column(String(50))
    C_ID = Column(BigInteger(), ForeignKey('color.ID'))
    Deleted = Column(Boolean, default=False)
    colors = relationship("t_Color", back_populates="scheme_lines")
    schemes = relationship("t_Paint_Scheme", back_populates="lines")

    def __repr__(self):
        return "Id = {}\nPS_ID = {}\nLabel = {}\nC_ID = {}\nDeleted{}".format(str(self.ID),
                                                                              str(self.PS_ID),
                                                                              self.Label,
                                                                              str(self.C_ID),
                                                                              str(self.Deleted))


class t_Brush(Basic.base):
    __tablename__ = "brush"

    ID = Column(BigInteger, primary_key=True)
    Name = Column(String(50))
    Description = Column(String)
    C_ID = Column(BigInteger(), ForeignKey('company.ID'))
    BT_ID = Column(BigInteger(), ForeignKey('brush_type.ID'))
    Owned = Column(Boolean, default=True)
    Deleted = Column(Boolean, default=False)
    company = relationship("t_Company", back_populates="brushes")
    brush_type = relationship("t_Brush_Type", back_populates="brushes")

    def __repr__(self):
        return "ID = {}\nName = {}\nDescription = {}\nC_ID = {}\nBT_ID = {}\nOwned = {}\nDeleted = {}".format(
            str(self.ID), self.Name, self.Description, str(self.C_ID), str(self.BT_ID), str(self.Owned),
            str(self.deleted))


class t_Brush_Type(Basic.base):
    __tablename__ = "brush_type"

    ID = Column(BigInteger, primary_key=True)
    Name = Column(String(50))
    Description = Column(String)
    Deleted = Column(Boolean, default=False)
    brushes = relationship("t_Brush", back_populates="brush_type")

    def __repr__(self):
        return "ID = {}\nName = {}\nDescription = {}\nDeleted = {}".format(
            str(self.ID), self.Name, self.Description, str(self.Deleted))


class zt_System_Setting(Basic.base):
    __tablename__ = "zt_system_setting"
    Sy_ID = Column(BigInteger, ForeignKey("system.ID", ondelete='CASCADE'), primary_key=True)
    Se_ID = Column(BigInteger, ForeignKey("setting.ID", ondelete='CASCADE'), primary_key=True)
    system = relationship("t_System", back_populates="settings")
    setting = relationship("t_Setting", back_populates="systems")

    def __repr__(self):
        return "Sy_ID = {}\nSe_ID = {}".format(str(self.Sy_ID), str(self.Se_ID))


def create_tables(meta, con, session):
    t_Company.__table__.create(session.bind)
    t_Color_Type.__table__.create(session.bind)
    t_System.__table__.create(session.bind)
    t_Setting.__table__.create(session.bind)
    t_Color.__table__.create(session.bind)
    t_Paint_Scheme.__table__.create(session.bind)
    t_Paint_Scheme_Line.__table__.create(session.bind)
    t_Brush_Type.__table__.create(session.bind)
    t_Brush.__table__.create(session.bind)
    zt_System_Setting.__table__.create(session.bind)

    meta.create_all(con)
    session.commit()
