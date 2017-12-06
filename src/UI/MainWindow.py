'''
Created on 06.12.2017

@author: mabelli
'''
from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QLabel

class MainWindow(QMainWindow):
    
    def __init__(self, dbService):
        super().__init__()
        
        self.dbService = dbService
        
        self.initUI()
        
    def initUI(self):
        label = QLabel(str(self.dbService.getSystems()), self)
        label.adjustSize()
        
        self.setWindowTitle("Tabletop Manager")
        self.move(300, 300)
        self.show()