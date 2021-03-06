class Mounter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("ErrorNotMounted", self.__mount_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from MountOperator import Operator
		self.__mount_operator = Operator(manager, editor)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		return False

	def __mount(self, data):
		gfile, error = data
		gfile.mount_enclosing_volume(self.__mount_operator, self.__async_ready_cb)
		return False

	def __check(self, uri):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__manager.emit, "check-file-type", uri, priority=PRIORITY_LOW)
		return False

	def __error(self, data):
		self.__manager.emit("gio-error", data)
		return False

	def __async_ready_cb(self, gfile, result):
		from gio import Error
		try:
			success = gfile.mount_enclosing_volume_finish(result)
			from gobject import idle_add, PRIORITY_LOW
			if success: idle_add(self.__check, gfile.get_uri(), priority=PRIORITY_LOW)
		except Error, e:
			from gobject import idle_add, PRIORITY_LOW
			idle_add(self.__error, (gfile, e), priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__destroy, priority=PRIORITY_LOW)
		return False

	def __mount_cb(self, manager, data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__mount, data, priority=PRIORITY_LOW)
		return False
