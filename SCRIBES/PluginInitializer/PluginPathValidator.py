from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "validate-path", self.__validate_cb)
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

	def __validate(self, plugin_path):
		try:
			from os.path import join, exists
			filename = join(plugin_path, "__init__.py")
			if not exists(filename): raise ValueError
			from gobject import idle_add
			idle_add(self.__manager.emit, "update-python-path", plugin_path)
		except ValueError:
			from gobject import idle_add
			idle_add(self.__manager.emit, "plugin-path-error", plugin_path)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __validate_cb(self, manager, plugin_path):
		from gobject import idle_add
		idle_add(self.__validate, plugin_path)
		return False
