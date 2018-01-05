'''
Created on 08.12.2017

@author: mabelli
'''
from sqlalchemy.sql import *
from Database.Tables import t_Color, t_Color_Type, t_Company
from Database.Basic import view

vUIColorSelect = select([t_Color.Name, t_Company.Name.label("Company"), t_Color_Type.Name.label("Color type"),\
                          t_Color.InStock, t_Color.Owned]).select_from(t_Color.join(t_Company).join(t_Color_Type))

# the ORM would appreciate this
assert stuff_view.primary_key == [stuff_view.c.id]