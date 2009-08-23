class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("plugin-path-error", self.__error_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __create(self, plugin_path):
		try:
			# Can only create plugin path in home folder.
			if not plugin_path.startswith(self.__editor.home_folder): raise ValueError
			self.__manager.emit("create-plugin-path", plugin_path)
		except ValueError:
			self.__manager.emit("plugin-path-not-found-error", plugin_path)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __error_cb(self, manager, plugin_path):
		from gobject import idle_add
		idle_add(self.__create, plugin_path)
		return False