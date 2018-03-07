'''
.. module:: Tabletopmanager
    :plattform: windows
    :sysnopsis: this is the main class of this project
    
.. moduleauthor:: Max Belli <mbegameacc@gmail.com>

Created on 06.12.2017

@author: mabelli
'''
import sys

from PyQt5.QtWidgets import QApplication

from Database.DBService import DBService
from UI.MainWindow import MainWindow

lang = "eng"


def main():
    """This is the main function of this class
    Args: 
        none
    """
    db = DBService()
    app = QApplication(sys.argv)
    UI = MainWindow(db, lang)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
