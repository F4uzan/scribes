from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"color": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"show": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"database-updated": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-whitespaces": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from WhitespaceDrawer import Drawer
		Drawer(editor, self)
		from DatabaseReader import Reader
		Reader(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def destroy(self):
		self.emit("destroy")
		del self
		return
