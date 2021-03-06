from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "plugin-path-error", self.__error_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __create(self, plugin_path):
		try:
			# Can only create plugin path in home folder.
			if not plugin_path.startswith(self.__editor.home_folder): raise ValueError
			from gobject import idle_add
			idle_add(self.__manager.emit, "create-plugin-path", plugin_path)
		except ValueError:
			from gobject import idle_add
			idle_add(self.__manager.emit, "plugin-path-not-found-error", plugin_path)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __error_cb(self, manager, plugin_path):
		from gobject import idle_add
		idle_add(self.__create, plugin_path)
		return False
