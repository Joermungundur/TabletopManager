'''
Created on 06.12.2017

@author: mabelli
'''
import sys
from PyQt5.QtWidgets import QApplication
from UI.MainWindow import MainWindow
from Database.DBService import DBService

def main():
    db = DBService()
    app = QApplication(sys.argv)
    UI = MainWindow(db)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()