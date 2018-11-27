import re

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QTableWidget, \
    QAbstractItemView, QHeaderView, QTableWidgetItem

from UI.Constants import Strings
from UI.Parents.PanelMaster import PanelMaster


class BrushPanel(PanelMaster):
    filter = dict(
        name="",
        company="",
        brushType="",
        owned=""
    )

    def __init__(self, dbService, lang):
        super().__init__(dbService, lang)

        self.brushes = self.db.get_full_brushes()
        self.company, self.brushType = self._get_search_criterions(self.brushes, self.lang)
        self.buttonBar = self._create_button_layout(self.lang)
        self.tb_brush = self._create_brushTable(self.lang)
        self.tf_name, self.cb_company, self.cb_brushType, self.cb_owned, \
            self. filterLayout = self._create_filterLayout(self.lang)
        self.initUI()

    def initUI(self):

        self.mainLayout.addLayout(self.filterLayout)
        center = QHBoxLayout(self)
        center.addWidget(self.tb_brush)
        center.addLayout(self.buttonBar)
        self.mainLayout.addLayout(center)

        self._fill_brushTable(self.brushes, self.tb_brush)

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

        lbl_brushType = QLabel(Strings.str_LABEL_BRUSH_TYPE.get(lang))
        cb_brushType = QComboBox(self)
        cb_brushType.addItems(self.brushType)
        cb_brushType.currentIndexChanged.connect(self._filter)

        cb_owned = QCheckBox(Strings.str_LABEL_OWNED.get(lang))
        cb_owned.setTristate(True)
        cb_owned.setCheckState(1)
        cb_owned.stateChanged.connect(self._filter)

        layout.addWidget(lbl_name)
        layout.addWidget(tf_name)

        layout.addWidget(lbl_company)
        layout.addWidget(cb_company)

        layout.addWidget(lbl_brushType)
        layout.addWidget(cb_brushType)

        layout.addWidget(cb_owned)

        layout.addStretch(1)

        return tf_name, cb_company, cb_brushType, cb_owned, layout

    def _create_brushTable(self, lang):
        headers = [Strings.str_LABEL_NAME.get(lang),
                   Strings.str_LABEL_COMPANY.get(lang),
                   Strings.str_LABEL_BRUSH_TYPE.get(lang),
                   Strings.str_LABEL_OWNED.get(lang)]

        tb_table = QTableWidget(self)
        tb_table.setRowCount(len(self.brushes))
        tb_table.setColumnCount(len(headers))

        tb_table.verticalHeader().setVisible(False)
        tb_table.setHorizontalHeaderLabels(headers)
        tb_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        tb_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        tb_table.setSortingEnabled(True)

        tb_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        return tb_table

    def _get_search_criterions(self, colors, lang):
        company = [Strings.str_LABEL_ALL.get(lang)]
        brushType = [Strings.str_LABEL_ALL.get(lang)]
        for entry in colors:
            if entry.Company_name not in company:
                company.append(entry.Company_name)
            if entry.Brush_type not in brushType:
                brushType.append(entry.Brush_type)

        return company, brushType

    def _fill_brushTable(self, brushes, tb_brush):
        for i in range(len(brushes)):
            brush = brushes[i]
            tb_brush.setItem(i, 0, QTableWidgetItem(brush.Name))
            tb_brush.setItem(i, 1, QTableWidgetItem(brush.Company_name))
            tb_brush.setItem(i, 2, QTableWidgetItem(brush.Brush_type))
            cb_owned = QCheckBox(tb_brush)
            cb_owned.setChecked(brush.Owned)
            tb_brush.setCellWidget(i, 3, cb_owned)

    def _filter(self):
        sender = self.sender()

        if sender == self.tf_name:
            self._set_filter("name", sender.text())
        elif sender == self.cb_company:
            if re.match(sender.currentText(), Strings.str_LABEL_ALL.get(self.lang)):
                self._set_filter("company", ".*")
            else:
                self._set_filter("company", sender.currentText())
        elif sender == self.cb_brushType:
            if re.match(sender.currentText(), Strings.str_LABEL_ALL.get(self.lang)):
                self._set_filter("brushType", ".*")
            else:
                self._set_filter("brushType", sender.currentText())
        elif sender == self.cb_owned:
            self._set_filter("owned", sender.checkState())

        filtered_brushes = []
        for brush in self.brushes:
            if self._match_filter_with_brush(self.filter, brush):
                filtered_brushes.append(brush)

        self.tb_brush.setRowCount(len(filtered_brushes))
        self._fill_brushTable(filtered_brushes, self.tb_brush)

    def _match_filter_with_brush(self, my_filter, brush):
        if my_filter["name"].lower() not in brush.Name.lower():
            return False
        if not re.match(my_filter["company"].lower(), brush.Company_name.lower()):
            return False
        if not re.match(my_filter["brushType"].lower(), brush.Brush_type.lower()):
            return False
        # checkBox Tristate : 0 = True, 1 = None, 2 = False
        if (my_filter["owned"] == 2 and brush.Owned is False) or \
                (my_filter["owned"] == 0 and brush.Owned is True):
            return False
        return True

    def _new(self):
        pass

    def _edit(self):
        pass

    def _del(self):
        pass

    def reload(self):
        self.brushes = self.db.get_full_brushes()
        self.company, self.brushType = self._get_search_criterions(self.brushes, self.lang)
        self._fill_brushTable(self.brushes, self.tb_brush)
