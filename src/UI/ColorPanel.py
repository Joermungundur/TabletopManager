'''
Created on 13.12.2017

@author: mabelli
'''
import re
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox,\
    QCheckBox, QTableWidget, QLineEdit, QHeaderView, QPushButton, QTableWidgetItem, \
    QAbstractItemView
    
from UI.Constants import Strings

class ColorPanel(QWidget):
    
    filter = {"name": "",
              "company": ".*",
              "colorType": ".*",
              "owned": 0,
              "inStock": 0}
    
    def __init__(self, dbService, lang):
        super().__init__()
        
        self.db = dbService
        self.lang = lang
        self.colors = self.db.get_full_colors()
        self.company, self.colorType = self._get_search_criterions(self.colors, self.lang)
        self.initUI()
    
    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.tf_name, self.cb_company, self.cb_colorType, self.cb_owned,\
            self.cb_inStock, self.filterLayout = self._create_filterLayout(self.lang)
        self.colorTable = self._create_colorTable(self.lang)
        self.saveButton, self.buttonBar = self._create_buttonBar(self.lang)
        
        self.mainLayout.addLayout(self.filterLayout)
        self.mainLayout.addWidget(self.colorTable)
        self.mainLayout.addLayout(self.buttonBar)
        
        self._fill_colorTable(self.colors, self.colorTable)
        
        return
    
    def _create_filterLayout(self, lang):
        layout = QHBoxLayout()
        
        lbl_name = QLabel(Strings.str_LABEL_NAME.get(lang))
        tf_name = QLineEdit(self)
        tf_name.textChanged.connect(self._filter)
        
        lbl_company = QLabel(Strings.str_LABEL_COMPANY.get(lang))
        cb_company = QComboBox(self)
        cb_company.addItems(self.company)
        cb_company.currentIndexChanged.connect(self._filter)
        
        lbl_colorType = QLabel(Strings.str_LABEL_COLOR_TYPE.get(lang))
        cb_colorType = QComboBox(self)
        cb_colorType.addItems(self.colorType)
        cb_colorType.currentIndexChanged.connect(self._filter)
        
        cb_owned = QCheckBox(Strings.str_LABEL_OWNED.get(lang))
        cb_owned.setTristate(True)
        cb_owned.stateChanged.connect(self._filter)
        
        cb_inStock = QCheckBox(Strings.str_LABEL_IN_STOCK.get(lang))
        cb_inStock.setTristate(True)
        cb_inStock.stateChanged.connect(self._filter)
        
        layout.addWidget(lbl_name)
        layout.addWidget(tf_name)
        
        layout.addWidget(lbl_company)
        layout.addWidget(cb_company)
        
        layout.addWidget(lbl_colorType)
        layout.addWidget(cb_colorType)
        
        layout.addWidget(cb_owned)
        layout.addWidget(cb_inStock)
        
        layout.addStretch(1)
        
        return tf_name, cb_company, cb_colorType, cb_owned, cb_inStock, layout
    
    def _create_colorTable(self, lang):
        headers = [Strings.str_LABEL_NAME.get(lang),
                   Strings.str_LABEL_COMPANY.get(lang),
                   Strings.str_LABEL_COLOR_TYPE.get(lang),
                   Strings.str_LABEL_OWNED.get(lang),
                   Strings.str_LABEL_IN_STOCK.get(lang)]
        
        table = QTableWidget(self)
        table.setRowCount(len(self.colors))
        table.setColumnCount(len(headers))
        
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setSortingEnabled(True)
        
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        return table
    
    def _create_buttonBar(self, lang):
        buttonBar = QHBoxLayout()
        
        saveButton = QPushButton(Strings.str_LABEL_SAVE.get(lang))
        
        buttonBar.addStretch(1)
        buttonBar.addWidget(saveButton)
        
        return saveButton, buttonBar
    
    def _get_search_criterions(self, colors, lang):
        company = [Strings.str_LABEL_ALL.get(lang)]
        colorType = [Strings.str_LABEL_ALL.get(lang)]
        for entry in colors:
            if entry[1] not in company:
                company.append(entry[1])
            if entry[2] not in colorType:
                colorType.append(entry[2])
        
        return company, colorType
   
    def _fill_colorTable(self, colors, colorTable):
        for i in range(len(colors)):
            color = colors[i]
            colorTable.setItem(i, 0, QTableWidgetItem(color[0]))
            colorTable.setItem(i, 1, QTableWidgetItem(color[1]))
            colorTable.setItem(i, 2, QTableWidgetItem(color[2]))
            cb_owned = QCheckBox(colorTable)
            cb_owned.setChecked(color[3])
            colorTable.setCellWidget(i, 3, cb_owned)
            cb_inStock = QCheckBox(colorTable)
            cb_inStock.setChecked(color[4])
            colorTable.setCellWidget(i, 4, cb_inStock)
            
    def _set_filter(self, key, value):
        self.filter[key] = value
        
    def _filter(self):
        sender = self.sender()
        print(self.filter)
       
        if sender == self.tf_name:
            self._set_filter("name", sender.text())
        elif sender == self.cb_company:
            if re.match(sender.currentText(), Strings.str_LABEL_ALL.get(self.lang)):
                self._set_filter("company", ".*")
            else:
                self._set_filter("company", sender.currentText())
        elif sender == self.cb_colorType:
            if re.match(sender.currentText(), Strings.str_LABEL_ALL.get(self.lang)):
                self._set_filter("colorType", ".*")
            else:
                self._set_filter("colorType", sender.currentText())
        elif sender == self.cb_owned:
            self._set_filter("owned", sender.checkState())
        elif sender == self.cb_inStock:
            self._set_filter("inStock", sender.checkState())
          
        filtered_colors = []
        for color in self.colors:
            if self._match_filter_with_color(self.filter, color):
                filtered_colors.append(color)
        
        self.colorTable.setRowCount(len(filtered_colors))
        self._fill_colorTable(filtered_colors, self.colorTable)
    
    def _match_filter_with_color(self, my_filter, color):
        if my_filter["name"] not in color[0]:
            return False
        if not re.match(my_filter["company"], color[1]):
            return False
        if not re.match(my_filter["colorType"], color[2]):
            return False
        if (my_filter["owned"] == 0 and color[3] is False) or \
            (my_filter["owned"] == 1 and color[3] is True):
            return False
        if (my_filter["inStock"] == 0 and color[4] is False) or \
            (my_filter["inStock"] == 1 and color[4] is True):
            return False
        return True 