class Monitor(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("loaded-file", self.__monitor_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__monitor_cb)
		self.__sigid4 = editor.connect("save-file", self.__busy_cb)
		self.__sigid5 = editor.connect_after("save-error", self.__nobusy_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__uri = ""
		self.__monitoring = False
		self.__busy = False
		self.__block = False
		return

	def __destroy(self):
		self.__unmonitor(self.__uri)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __monitor(self, uri):
		self.__unmonitor(self.__uri)
		if uri.startswith("file:///") is False: return False
		self.__uri = uri
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(uri, MONITOR_FILE, self.__changed_cb)
		self.__monitoring = True
		return False

	def __unmonitor(self, uri):
		if not uri: return False
		if self.__monitoring is False: return False
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		self.__monitoring = False
		return False

	def __reload(self):
		from URILoader.Manager import Manager
		Manager(self.__editor, self.__editor.uri, self.__editor.encoding)
		return False

	def __unblock(self):
		self.__block = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __monitor_cb(self, editor, uri, *args):
		from gobject import idle_add
		idle_add(self.__monitor, uri, priority=9999)
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__process, args, priority=9999)
		return False

	def __process(self, args):
		try:
			if not (args[-1] in (0,4)): return False
			if self.__block: return False
			self.__block = True
			from gobject import timeout_add
			timeout_add(500, self.__unblock)
			if self.__busy: raise ValueError
			timeout_add(10, self.__reload)
		except ValueError:
			self.__busy = False
		return False

	def __busy_cb(self, *args):
		self.__busy = True
		return False

	def __nobusy_cb(self, *args):
		self.__busy = False
		return False
