from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QTextEdit, QVBoxLayout

from Database.Tables import t_Color_Type
from UI.Constants import Strings
from UI.Parents.DialogMaster import DialogMaster


class AddTypeDialog(DialogMaster):
    def __init__(self, dbService, lang, parent=None):
        super(AddTypeDialog, self).__init__(dbService, lang, Strings.str_TITLE_NEW_TYPE.get(lang), parent)

        self._initUI()

    def _initUI(self):
        base = QVBoxLayout(self)

        self.txt_company_name, self.txt_company_description, content_layout = \
            self._build_content()
        buttons = self._mk_button_layout(self.lang)

        base.addLayout(content_layout)
        base.addSpacing(10)
        base.addLayout(buttons)

    def _build_content(self):
        layout = QFormLayout()

        lbl_name = QLabel(Strings.str_LABEL_NAME.get(self.lang))
        txt_name = QLineEdit()

        lbl_description = QLabel(Strings.str_LABEL_DESCRIPTION.get(self.lang))
        txt_description = QTextEdit()
        txt_description.resize(50, 60)

        layout.addRow(lbl_name, txt_name)
        layout.addRow(lbl_description, txt_description)

        return txt_name, txt_description, layout

    def _save(self):
        self.dbService.session.add(t_Color_Type(Name=self.txt_company_name.text(),
                                                Description=self.txt_company_description.toPlainText()))
        self.dbService.session.commit()
        self.parent.refresh_color_types()
        self.close()
