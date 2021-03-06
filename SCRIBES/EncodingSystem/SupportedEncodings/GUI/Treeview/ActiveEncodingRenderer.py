from gtk import CellRendererToggle

class Renderer(CellRendererToggle):

	def __init__(self, manager, editor):
		CellRendererToggle.__init__(self)
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.connect("toggled", self.__toggled_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_widget("TreeView")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __toggle(self, path):
		self.__view.set_property("sensitive", False)
		model = self.__view.get_model()
		treemodelrow = model[path]
		treemodelrow[0] = not treemodelrow[0]
		self.__manager.emit("toggled-path", path)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __toggled_cb(self, renderer, path):
		from gobject import idle_add
		idle_add(self.__toggle, path)
		return False
