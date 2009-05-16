class Checker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("check-remote-uri", self.__check_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __check(self, uri):
		self.__manager.emit("read-uri", uri)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__check, uri)
		return False
