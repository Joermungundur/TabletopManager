import re

from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout, \
    QLineEdit, QLabel, QComboBox

from Database.Tables import t_Color, t_Company
from UI.Constants import Strings
from UI.Dialogs.ColorDialog import ColorDialog
from UI.Parents.PanelMaster import PanelMaster


class ColorPanel(PanelMaster):
    filter = dict(
        name="",
        company=".*",
        colorType=".*",
        owned=1,
        inStock=1
    )

    def __init__(self, dbService, lang):
        super().__init__(dbService, lang)

        self.colors = self.db.get_full_colors()
        self.company, self.colorType = self._get_search_criterions(self.colors, self.lang)
        self.buttonBar = self._create_buttonBar(self.lang)
        self.tb_color = self._create_colorTable(self.lang)
        self.tf_name, self.cb_company, self.cb_colorType, self.cb_owned, \
        self.cb_inStock, self.filterLayout = self._create_filterLayout(self.lang)
        self.initUI()

    def initUI(self):

        self.mainLayout.addLayout(self.filterLayout)
        center = QHBoxLayout(self)
        center.addWidget(self.tb_color)
        center.addLayout(self.buttonBar)
        self.mainLayout.addLayout(center)

        self._fill_colorTable(self.colors, self.tb_color)

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
        cb_owned.setCheckState(1)
        cb_owned.stateChanged.connect(self._filter)

        cb_inStock = QCheckBox(Strings.str_LABEL_IN_STOCK.get(lang))
        cb_inStock.setTristate(True)
        cb_inStock.setCheckState(1)
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
                   Strings.str_LABEL_ARTICLE_ID.get(lang),
                   Strings.str_LABEL_OWNED.get(lang),
                   Strings.str_LABEL_IN_STOCK.get(lang)]

        tb_table = QTableWidget(self)
        tb_table.setRowCount(len(self.colors))
        tb_table.setColumnCount(len(headers))

        tb_table.verticalHeader().setVisible(False)
        tb_table.setHorizontalHeaderLabels(headers)
        tb_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        tb_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        tb_table.setSortingEnabled(True)

        tb_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        tb_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        return tb_table

    def _new(self):
        cp = ColorDialog(self.db, self.lang, parent=self)
        cp.exec_()

    def _edit(self):
        row = self.tb_color.currentRow()
        if row is not -1:
            rown = self.tb_color.item(row, 0).text()
            name = self.colors[row].Name
            if re.match(rown, name):
                cp = ColorDialog(self.db, self.lang, self.colors[row], self)
                cp.exec_()

    def _del(self):
        session = self.db.session
        row = self.tb_color.currentRow()
        color_name = self.tb_color.item(row, 0).text()
        company_name = self.tb_color.item(row, 1).text()
        for company in session.query(t_Company.ID).filter(t_Company.Name == company_name):
            session.query(t_Color).filter(
                t_Color.Name == color_name,
                t_Color.C_ID == company.ID).update(
                {"Deleted": True})
            session.commit()
        self.reload()

    def _get_search_criterions(self, colors, lang):
        company = [Strings.str_LABEL_ALL.get(lang)]
        colorType = [Strings.str_LABEL_ALL.get(lang)]
        for entry in colors:
            if entry.Company_name not in company:
                company.append(entry.Company_name)
            if entry.Color_type not in colorType:
                colorType.append(entry.Color_type)

        return company, colorType

    def _fill_colorTable(self, colors, tb_color):
        for i in range(len(colors)):
            color = colors[i]
            tb_color.setItem(i, 0, QTableWidgetItem(color.Name))
            tb_color.setItem(i, 1, QTableWidgetItem(color.Company_name))
            tb_color.setItem(i, 2, QTableWidgetItem(color.Color_type))
            tb_color.setItem(i, 3, QTableWidgetItem(color.ID_Num))
            cb_owned = QCheckBox(tb_color)
            cb_owned.setChecked(color.Owned)
            tb_color.setCellWidget(i, 4, cb_owned)
            cb_inStock = QCheckBox(tb_color)
            cb_inStock.setChecked(color.InStock)
            tb_color.setCellWidget(i, 5, cb_inStock)

    def _set_filter(self, key, value):
        self.filter[key] = value

    def _filter(self):
        sender = self.sender()

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

        self.tb_color.setRowCount(len(filtered_colors))
        self._fill_colorTable(filtered_colors, self.tb_color)

    def _match_filter_with_color(self, my_filter, color):
        if my_filter["name"].lower() not in color.Name.lower():
            return False
        if not re.match(my_filter["company"].lower(), color.Company_name.lower()):
            return False
        if not re.match(my_filter["colorType"].lower(), color.Color_type.lower()):
            return False
        # checkBox Tristate : 0 = True, 1 = None, 2 = False
        if (my_filter["owned"] == 2 and color.Owned is False) or \
                (my_filter["owned"] == 0 and color.Owned is True):
            return False
        if (my_filter["inStock"] == 2 and color.InStock is False) or \
                (my_filter["inStock"] == 0 and color.InStock is True):
            return False
        return True

    def reload(self):
        self.colors = self.db.get_full_colors()
        self.company, self.colorType = self._get_search_criterions(self.colors, self.lang)
        self._fill_colorTable(self.colors, self.tb_color)
