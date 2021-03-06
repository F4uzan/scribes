class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("show-error", self.__update_cb)
		self.__sigid3 = editor.connect("show-info", self.__update_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.gui.get_widget("MessageLabel")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, message):
		self.__label.set_label(message)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, editor, title, message, window, busy):
		from gobject import idle_add
		idle_add(self.__update, message, priority=9999)
		return False
