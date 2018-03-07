'''
Created on 06.12.2017

@author: mabelli
'''
from Database.DBService import DBService
from Database.Tables import t_Color


def main():
    db = DBService()
    db.drop_tables()
    db.create_tables()
    db.create_dataBase()


if __name__ == "__main__":
    main()
