import re

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QCheckBox, QTableWidget, QAbstractItemView, QHeaderView, \
    QTableWidgetItem, QComboBox

from UI.Constants import Strings
from UI.Parents.PanelMaster import PanelMaster


class PaintSchemePanel(PanelMaster):
    filter = dict(
        name="",
        system=".*",
        active=1
    )

    def __init__(self, dbService, lang):
        super().__init__(dbService, lang)

        self.paint_schemes = self.db.get_full_paint_schemes()
        self.system_name = self._get_search_criterions(self.paint_schemes, lang)
        self.buttonBar = self._create_button_layout(self.lang)
        self.tb_paint_schemes = self._create_paint_schemeTable(self.lang)
        self.tf_name, self.cb_system, self.cb_active, self.filterLayout = self._create_filterLayout(self.lang)
        self.initUI()

    def initUI(self):

        self.mainLayout.addLayout(self.filterLayout)
        center = QHBoxLayout(self)
        center.addWidget(self.tb_paint_schemes)
        center.addLayout(self.buttonBar)
        self.mainLayout.addLayout(center)

        self._fill_paint_scheme_table(self.paint_schemes, self.tb_paint_schemes)

        return

    def _create_filterLayout(self, lang):
        layout = QHBoxLayout()

        lbl_name = QLabel(Strings.str_LABEL_NAME.get(lang))
        tf_name = QLineEdit(self)
        tf_name.textChanged.connect(self._filter)

        lbl_system = QLabel(Strings.str_LABEL_SYSTEM.get(lang))
        cb_system = QComboBox(self)
        cb_system.addItems(self.system_name)
        cb_system.currentIndexChanged.connect(self._filter)

        cb_active = QCheckBox(Strings.str_LABEL_ACTIVE.get(lang))
        cb_active.setTristate(True)
        cb_active.setCheckState(1)
        cb_active.stateChanged.connect(self._filter)

        layout.addWidget(lbl_name)
        layout.addWidget(tf_name)

        layout.addWidget(lbl_system)
        layout.addWidget(cb_system)

        layout.addWidget(cb_active)

        layout.addStretch(1)

        return tf_name, cb_system, cb_active, layout

    def _create_paint_schemeTable(self, lang):
        headers = [Strings.str_LABEL_NAME.get(lang),
                   Strings.str_LABEL_SYSTEM.get(lang),
                   Strings.str_LABEL_STEPS.get(lang),
                   Strings.str_LABEL_ACTIVE.get(lang)]

        tb_table = QTableWidget(self)
        tb_table.setRowCount(len(self.paint_schemes))
        tb_table.setColumnCount(len(headers))

        tb_table.verticalHeader().setVisible(False)
        tb_table.setHorizontalHeaderLabels(headers)
        tb_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        tb_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        tb_table.setSortingEnabled(True)

        tb_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        tb_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        return tb_table

    def _new(self):
        pass

    def _edit(self):
        pass

    def _del(self):
        pass

    def _get_search_criterions(self, paint_schemes, lang):
        system = [Strings.str_LABEL_ALL.get(lang)]
        for entry in paint_schemes:
            if entry.System_name not in system:
                system.append(entry.System_name)

        return system

    def _fill_paint_scheme_table(self, paint_schemes, tb_paint_scheme):
        for i in range(len(paint_schemes)):
            scheme = paint_schemes[i]
            tb_paint_scheme.setItem(i, 0, QTableWidgetItem(scheme.name))
            tb_paint_scheme.setItem(i, 1, QTableWidgetItem(scheme.System_name))
            tb_paint_scheme.setItem(i, 2, QTableWidgetItem(scheme.Steps))
            cb_active = QCheckBox(tb_paint_scheme)
            cb_active.setChecked(scheme.active)
            tb_paint_scheme.setCellWidget(i, 3, cb_active)

    def _filter(self):
        sender = self.sender()

        if sender == self.tf_name:
            self._set_filter("name", sender.text())
        elif sender== self.cb_system:
            if re.match(sender.currentText(), Strings.str_LABEL_ALL.get(self.lang)):
                self._set_filter("system", ".*")
            else:
                self._set_filter("system", sender.currentText())
        elif sender == self.cb_active:
            self._set_filter("active", sender.checkState())

        filtered_paint_schemes = []
        for scheme in self.paint_schemes:
            if self._match_filter_with_paint_scheme(self.filter, scheme):
                filtered_paint_schemes.append(scheme)

        self.tb_paint_schemes.setRowCount(len(filtered_paint_schemes))
        self._fill_paint_scheme_table(filtered_paint_schemes, self.tb_paint_schemes)

    def _match_filter_with_paint_scheme(self, my_filter, paint_scheme):
        if my_filter["name"].lower() not in paint_scheme.name.lower():
            return False
        if not re.match(my_filter["system"].lower(), paint_scheme.system_name.lower()):
            return False
        if (my_filter["active"] == 2 and paint_scheme.Active is False) or (my_filter["active"] == 0 and paint_scheme.Active is True):
            return False
        return True

    def reload(self):
        self.paint_schemes = self.db.get_full_paint_schemes()
        self.system_name = self._get_search_criterions(self.paint_schemes, self.lang)
        self._fill_paint_scheme_table(self.paint_schemes, self.tb_paint_schemes)