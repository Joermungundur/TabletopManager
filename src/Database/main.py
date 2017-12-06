'''
Created on 06.12.2017

@author: mabelli
'''
from Database.DBService import DBService

def main():
    db = DBService()
    db.dropTables()
    db.createTables()
    db.createDataBase()
    print("DB Created")
    print(db.getSystems())
    print(db.getCompanies())
        
    
   
if __name__ == "__main__":
    main();   
