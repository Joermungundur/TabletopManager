'''
Created on 06.12.2017

@author: mabelli
'''
from Database.DBService import DBService

def main():
    db = DBService()
#     db.createTables()
#     db.createDataBase()
#     print("DB Created")
    systems = db.getSystems()
    for sys in systems:
        print(sys)
   
if __name__ == "__main__":
    main();   
