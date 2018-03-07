from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from UI.Constants import Strings


class PanelMaster(QWidget):

    def __init__(self, dbService, lang):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)
        self.db = dbService
        self.lang = lang

        self.buttonBar = self._create_buttonBar(self.lang)

    def _create_buttonBar(self, lang):
        buttonBar = QVBoxLayout()

        btn_new = QPushButton(Strings.str_LABEL_NEW.get(lang))
        btn_new.clicked.connect(self._new)

        btn_edit = QPushButton(Strings.str_LABEL_EDIT.get(lang))
        btn_edit.clicked.connect(self._edit)

        btn_delete = QPushButton(Strings.str_LABEL_DELETE.get(lang))
        btn_delete.clicked.connect(self._del)

        btn_refresh = QPushButton(Strings.str_LABEL_REFRESH.get(lang))
        btn_refresh.clicked.connect(self.reload)

        buttonBar.addSpacing(30)
        buttonBar.addWidget(btn_new)
        buttonBar.addWidget(btn_edit)
        buttonBar.addWidget(btn_delete)
        buttonBar.addSpacing(15)
        buttonBar.addWidget(btn_refresh)

        buttonBar.addStretch(1)

        return buttonBar

    def initUI(self):
        pass

    def _new(self):
        pass

    def _edit(self):
        pass

    def _del(self):
        pass

    def reload(self):
        pass
