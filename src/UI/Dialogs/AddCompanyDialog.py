from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QFormLayout, QTextEdit

from Database.Tables import t_Company
from UI.Constants import Strings
from UI.Parents.DialogMaster import DialogMaster


class AddCompanyDialog(DialogMaster):
    def __init__(self, dbService, lang, parent=None):
        super(AddCompanyDialog, self).__init__(dbService, lang, Strings.str_TITLE_NEW_COMPANY.get(lang), parent)

        self._initUI()

    def _initUI(self):
        base = QVBoxLayout(self)

        self.txt_company_name, self.txt_company_description, self.txt_company_website, content_layout = \
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

        lbl_website = QLabel(Strings.str_LABEL_WEBSITE.get(self.lang))
        txt_website = QLineEdit()

        layout.addRow(lbl_name, txt_name)
        layout.addRow(lbl_description, txt_description)
        layout.addRow(lbl_website, txt_website)

        return txt_name, txt_description, txt_website, layout

    def _save(self):
        self.dbService.session.add(t_Company(Name=self.txt_company_name.text(),
                                             Description=self.txt_company_description.toPlainText(),
                                             Website=self.txt_company_website.text()))
        self.dbService.session.commit()
        self.parent.refresh_companies()
        self.close()
