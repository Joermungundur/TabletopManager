from UI.Constants import Strings
from UI.Parents.DialogMaster import DialogMaster


class BrushDialog(DialogMaster):
    def __init__(self, dbService, lang, brush=None, parent=None):
        super(BrushDialog, self).__init__(dbService,lang, Strings.str_TITLE_NEW_BRUSH.get(lang) if brush is None else
                                          Strings.str_TITLE_EDIT_BRUSH.get(lang), parent)
        self.result = ""
        self.brush = brush
        self.companies = self.dbService.get_companies()
        self.brushTypes = self.dbService.get_brush_type()

        self._initUI()
        if brush is not None:
            self._load_brush(brush)
