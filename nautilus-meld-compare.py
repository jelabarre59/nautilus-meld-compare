import os
import nautilus
import locale
import gettext

APP = 'nautilus-meld-compare'

MELD_BIN_PATH = '/usr/bin/meld'

class MedlDiffExtension(nautilus.MenuProvider):
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        gettext.bindtextdomain(APP)
        gettext.textdomain(APP)
        self._ = gettext.gettext
        return

    def _open_meld(self, files):
	if len(files) >= 2:
            f = files[0].get_uri().replace("%s://" %(files[0].get_uri_scheme()), "")
            f = f.replace("%20", " ")
            s = files[1].get_uri().replace("%s://" %(files[1].get_uri_scheme()), "")
            s = s.replace("%20", " ")
        if len(files) == 2:
            os.system('%s "%s" "%s" &' %(MELD_BIN_PATH, f, s))
        elif len(files) == 3:
            t = files[2].get_uri().replace("%s://" %(files[2].get_uri_scheme()), "")
            t = t.replace("%20", " ")
            os.system('%s "%s" "%s" "%s" &' %(MELD_BIN_PATH, f, s, t))
        return 

    def menu_activate_cb(self, menu, files):
        self._open_meld(files)
        return

    def get_file_items(self, window, files):
        if len(files) != 2 and len(files) != 3:
            return

        compare = 0

        if len(files) == 2:
           if files[0].is_directory() and files[1].is_directory():
               compare = 1
           elif not files[0].is_directory() and not files[1].is_directory():
               compare = 1
        elif len(files) == 3:
           if files[0].is_directory() and files[1].is_directory() and files[2].is_directory():
               compare = 1
           elif not files[0].is_directory() and not files[1].is_directory() and not files[2].is_directory():
               compare = 1

        if compare:
            if len(files) == 2:
                item = nautilus.MenuItem('NautilusPython::meld_compare_file_item', self._("Compare content"), self._("Compare `%(firstFilename)s` and `%(secoundFilename)s` in Meld") % {'firstFilename': files[0].get_name(), 'secoundFilename': files[1].get_name()})
            elif len(files) == 3:
                item = nautilus.MenuItem('NautilusPython::meld_compare_file_item', self._("Compare content"), self._("Compare `%(firstFilename)s`, `%(secoundFilename)s` and `%(thirdFilename)s` in Meld") %{'firstFilename': files[0].get_name(), 'secoundFilename': files[1].get_name(), 'thirdFilename': files[2].get_name()})
            item.connect('activate', self.menu_activate_cb, files)
            return item,
