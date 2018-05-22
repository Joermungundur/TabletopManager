'''
Created on 18.01.2018

@author: mabelli
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, \
    QLabel, QLineEdit, QCheckBox, QComboBox, QGridLayout

from Database.Tables import t_Color
from UI.Constants import Strings, Helper
from UI.Dialogs.AddCompanyDialog import AddCompanyDialog
from UI.Dialogs.AddTypeDialog import AddTypeDialog
from UI.Parents.DialogMaster import DialogMaster


class ColorDialog(DialogMaster):
    def __init__(self, dbService, lang, color=None, parent=None):
        super(ColorDialog, self).__init__(dbService, lang, Strings.str_TITLE_NEW_COLOR.get(lang) if color is None else \
            Strings.str_TITLE_EDIT_COLOR.get(lang), parent)
        self.result = ""
        self.color = color
        self.companies = self._get_companies()
        self.colorTypes = self._get_colorTypes()

        self._initUI()
        if color is not None:
            self._load_color(color)

    def refresh_companies(self):
        self.companies = self._get_companies()
        self.cb_comp.clear()
        for company in self.companies:
            self.cb_comp.addItem(company.Name)

    def refresh_color_types(self):
        self.colorTypes = self._get_colorTypes()
        self.cb_type.clear()
        for type in self.colorTypes:
            self.cb_type.addItem(type.Name)

    def _initUI(self):
        base = QVBoxLayout(self)

        widget = QHBoxLayout()

        self.txt_name, self.cb_comp, self.cb_type, left = self._mk_left_layout(
            self.lang,
            self.companies,
            self.colorTypes)
        self.txt_article_id, self.cb_owned, self.cb_inSto, right = self._mk_right_layout(self.lang)

        buttons = self._mk_button_layout(self.lang)

        widget.addLayout(left)
        widget.addSpacing(5)
        widget.addLayout(right)

        base.addLayout(widget)
        base.addSpacing(10)
        base.addLayout(buttons)

    def _load_color(self, color):
        self.txt_name.setText(color.Name)
        self.cb_comp.setCurrentIndex(self.cb_comp.findText(color.Company_name,
                                                           Qt.MatchExactly))
        self.cb_type.setCurrentIndex(self.cb_type.findText(color.Color_type,
                                                           Qt.MatchExactly))
        self.txt_article_id.setText(color.ID_Num)
        self.cb_owned.setChecked(color.Owned)
        self.cb_inSto.setChecked(color.InStock)

    def _get_companies(self):
        return self.dbService.get_companies()

    def _get_colorTypes(self):
        return self.dbService.get_color_type()

    def _mk_left_layout(self, lang, companies, colorTypes):
        ret = QVBoxLayout()

        lbl_name = QLabel(Strings.str_LABEL_NAME.get(lang))
        txt_name = QLineEdit()

        company_grid_layout = QGridLayout()
        lbl_comp = QLabel(Strings.str_LABEL_COMPANY.get(lang))
        cb_comp = QComboBox()
        for company in companies:
            cb_comp.addItem(company.Name)
        btn_add_company = QPushButton("+")
        btn_add_company.clicked.connect(lambda _: self._add_company())
        company_grid_layout.addWidget(cb_comp, 0, 0, 1, 4)
        company_grid_layout.addWidget(btn_add_company, 0, 5)

        type_grid_layout = QGridLayout()
        lbl_type = QLabel(Strings.str_LABEL_COLOR_TYPE.get(lang))
        cb_type = QComboBox()
        for typ in colorTypes:
            cb_type.addItem(typ.Name)
        btn_add_type = QPushButton("+")
        btn_add_type.clicked.connect(lambda _: self._add_type())
        type_grid_layout.addWidget(cb_type, 0, 0, 1, 4)
        type_grid_layout.addWidget(btn_add_type, 0, 5)

        ret.addWidget(lbl_name)
        ret.addWidget(txt_name)
        ret.addSpacing(15)
        ret.addWidget(lbl_comp)
        ret.addLayout(company_grid_layout)
        ret.addSpacing(15)
        ret.addWidget(lbl_type)
        ret.addLayout(type_grid_layout)

        return txt_name, cb_comp, cb_type, ret

    def _mk_right_layout(self, lang):
        ret = QVBoxLayout()

        lbl_idNum = QLabel(Strings.str_LABEL_ARTICLE_ID.get(lang))
        txt_idNum = QLineEdit()

        cb_owned = QCheckBox(Strings.str_LABEL_OWNED.get(lang))
        cb_inSto = QCheckBox(Strings.str_LABEL_IN_STOCK.get(lang))

        ret.addWidget(lbl_idNum)
        ret.addWidget(txt_idNum)
        ret.addSpacing(36)
        ret.addWidget(cb_owned)
        ret.addSpacing(15 + 22)
        ret.addWidget(cb_inSto)
        ret.addStretch(1)

        return txt_idNum, cb_owned, cb_inSto, ret

    def _save(self):
        if self.color is not None:
            uid = self.color.ID
        else:
            uid = None
        name = self.txt_name.text()
        c_id = self._get_company_id(self.cb_comp.currentText())
        ct_id = self._get_colorType_id(self.cb_type.currentText())
        id_num = self.txt_article_id.text()
        owned = self.cb_owned.isChecked()
        inStock = self.cb_inSto.isChecked()

        if uid is None:
            self.dbService.session.add(t_Color(
                ID=uid,
                Name=name,
                C_ID=c_id,
                CT_ID=ct_id,
                ID_Num=id_num,
                Owned=owned,
                InStock=inStock))
        else:
            self.dbService.session.query(t_Color).filter_by(ID=uid).update({
                "ID": uid,
                "Name": name,
                "C_ID": c_id,
                "CT_ID": ct_id,
                "ID_Num": id_num,
                "Owned": owned,
                "InStock": inStock})
        self.dbService.session.commit()

        self.parent.reload()
        self.close()
        return

    def _get_company_id(self, company_name):
        return Helper.find_id(company_name, self.companies)

    def _get_colorType_id(self, colorType):
        return Helper.find_id(colorType, self.colorTypes)

    def get_result(self):
        return self.result

    def _add_company(self):
        AddCompanyDialog(self.dbService, self.lang, self).exec()

    def _add_type(self):
        AddTypeDialog(self.dbService, self.lang,self).exec()
