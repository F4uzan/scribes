class Updater(object):

	def __init__(self, editor, uri):
		self.__init_attributes(editor, uri)
		self.__sigid1 = editor.connect("close", self.__close_cb)
		self.__sigid2 = self.__window.connect("focus-out-event", self.__update_cb)
		self.__sigid3 = self.__window.connect("focus-in-event", self.__update_cb)
		self.__sigid4 = editor.connect("checking-file", self.__checking_cb)
		self.__sigid5 = editor.connect("load-error", self.__error_cb)
		self.__sigid6 = editor.connect("saved-file", self.__saved_cb)
		editor.register_object(self)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__uri = uri
		self.__window = editor.window
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__window)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__set_position_in_database()
		self.__editor.response()
		self.__window.hide()
		self.__editor.response()
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_position_in_database(self):
		self.__editor.response()
		xcoordinate, ycoordinate = self.__window.get_position()
		width, height = self.__window.get_size()
		is_maximized = False # self.__is_maximized
		uri = self.__uri if self.__uri else "<EMPTY>"
		maximized_position = (True, None, None, None, None)
		unmaximized_position = (False, width, height, xcoordinate, ycoordinate)
		window_position = maximized_position if is_maximized else unmaximized_position
		from SCRIBES.PositionMetadata import update_window_position_in_database
		update_window_position_in_database(str(uri), window_position)
		self.__editor.response()
		return False

	def __close_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set_position_in_database, priority=9999)
		return False

	def __checking_cb(self, editor, uri):
		self.__uri = uri
		return False

	def __error_cb(self, *args):
		self.__uri = None
		return False

	def __saved_cb(self, editor, uri, *args):
		self.__uri = uri
		return False