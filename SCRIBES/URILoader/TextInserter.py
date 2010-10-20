class Inserter(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("insert-text", self.__insert_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __insert(self, uri, string, encoding):
		try:
			if encoding is None: encoding = "utf-8"
			unicode_string = string.decode(encoding, "strict")
			utf8_string = unicode_string.encode("utf-8", "strict")
			self.__editor.textview.window.freeze_updates()
			self.__editor.refresh(True)
			self.__editor.textbuffer.set_text(utf8_string)
			self.__editor.refresh(True)
			self.__manager.emit("load-success", uri, encoding)
#			from gobject import timeout_add
#			timeout_add(125, self.__set_cursor_timeout)
		except:
			self.__manager.emit("insertion-error", uri, string)
		return False

	def __set_cursor(self):
		self.__editor.move_view_to_cursor(True)
		self.__editor.textview.window.thaw_updates()
		return False

	def __set_cursor_timeout(self):
		from gobject import idle_add
		idle_add(self.__set_cursor)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __insert_cb(self, manager, uri, string, encoding):
		from gobject import idle_add
		idle_add(self.__insert, uri, string, encoding, priority=99999)
		return False
