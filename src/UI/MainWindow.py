'''
Created on 06.12.2017

@author: mabelli
'''
from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QTabWidget

from UI.Panels.BrushPanel import BrushPanel
from UI.Panels.ColorPanel import ColorPanel
from UI.Constants import Strings

class MainWindow(QMainWindow):
    
    def __init__(self, dbService, lang):
        super().__init__()
        
        self.lang = lang
        self.dbService = dbService
        self.appSize = [1000, 1000]
        self.initUI()
        
    def initUI(self):
        
        self.tabs = QTabWidget(self)
        self.tabs.resize(self.appSize[0], self.appSize[1])
        self.colorPanel = ColorPanel(self.dbService, self.lang)
        self.brushPanel = BrushPanel(self.dbService, self.lang)
        self.tabs.addTab(self.colorPanel, Strings.str_LABEL_COLORS.get(self.lang))
        self.tabs.addTab(self.brushPanel, Strings.str_LABEL_BRUSHES.get(self.lang))
        
        self.setWindowTitle("Tabletop Manager")
        self.move(100, 100)
        #self.resize(self.appSize[0], self.appSize[1])
        self.setFixedSize(self.appSize[0], self.appSize[1])
        self.show()
        
        