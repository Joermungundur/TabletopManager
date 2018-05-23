from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton

from UI.Constants import Strings


class DialogMaster(QDialog):
    def __init__(self, dbService, lang, title=None, parent=None):
        super(DialogMaster, self).__init__(parent)
        self.dbService = dbService
        self.lang = lang
        self.parent = parent

        self.setWindowTitle(title)

    def _initUI(self):
        raise NotImplementedError

    def _save(self):
        raise NotImplementedError

    def _mk_button_layout(self, lang):
        ret = QHBoxLayout()

        btn_ok = QPushButton("Ok")
        btn_ok.resize(40, 30)
        btn_ok.clicked.connect(lambda _: self._save())

        btn_cancel = QPushButton(Strings.str_LABEL_CANCEL.get(lang))
        btn_cancel.resize(40, 30)
        btn_cancel.clicked.connect(lambda _: self.close())

        ret.addStretch(1)
        ret.addWidget(btn_ok)
        ret.addSpacing(10)
        ret.addWidget(btn_cancel)

        return ret
