from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from UI.Constants import Strings


class PanelMaster(QWidget):

    def __init__(self, dbService, lang):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)
        self.db = dbService
        self.lang = lang

        self.buttonBar = self._create_button_layout(self.lang)

    def _create_button_layout(self, lang):
        button_bar = QVBoxLayout()

        btn_new = QPushButton(Strings.str_LABEL_NEW.get(lang))
        btn_new.clicked.connect(self._new)

        btn_edit = QPushButton(Strings.str_LABEL_EDIT.get(lang))
        btn_edit.clicked.connect(self._edit)

        btn_delete = QPushButton(Strings.str_LABEL_DELETE.get(lang))
        btn_delete.clicked.connect(self._del)

        btn_refresh = QPushButton(Strings.str_LABEL_REFRESH.get(lang))
        btn_refresh.clicked.connect(self.reload)

        button_bar.addSpacing(30)
        button_bar.addWidget(btn_new)
        button_bar.addWidget(btn_edit)
        button_bar.addWidget(btn_delete)
        button_bar.addSpacing(15)
        button_bar.addWidget(btn_refresh)

        button_bar.addStretch(1)

        return button_bar

    def _set_filter(self, key, value):
        self.filter[key] = value

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
