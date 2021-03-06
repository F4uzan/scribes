from SCRIBES.SignalConnectionManager import SignalManager

class Validator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "valid-module", self.__validate_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __validate(self, module):
		try:
			class_name = getattr(module, "class_name")
			if not hasattr(module, class_name): raise ValueError
			PluginClass = getattr(module, class_name)
			if hasattr(PluginClass, "__init__") is False: raise ValueError
			if hasattr(PluginClass, "load") is False: raise ValueError
			if hasattr(PluginClass, "unload") is False: raise ValueError
			emit = self.__manager.emit 
			from gobject import idle_add
			idle_add(emit, "check-duplicate-plugins", (module, PluginClass))
		except ValueError:
			print module, " has an invalid plugin class"
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __validate_cb(self, manager, module):
		from gobject import idle_add
		idle_add(self.__validate, module)
		return False
