from SCRIBES.SignalConnectionManager import SignalManager

class Placer(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "checking-file", self.__checking_cb)
		self.connect(editor, "loaded-file", self.__loaded_cb, True)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__line_position = 0, 0
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __place_timeout(self):
		from gobject import idle_add
		idle_add(self.__place)
		return False

	def __place(self):
		line, index = self.__line_position
		iterator = self.__get_cursor_iterator(line)
		index = self.__get_cursor_index(iterator, index)
		iterator.set_line_index(index)
		self.__editor.response()
		self.__buffer.place_cursor(iterator)
		self.__editor.response()
		self.__editor.move_view_to_cursor(True)
		self.__editor.response()
		self.__editor.textview.window.thaw_updates()
		self.__editor.response()
		return False

	def __get_cursor_data(self):
		from SCRIBES.CursorMetadata import get_value
		self.__editor.response()
		position = get_value(self.__editor.uri)
		self.__editor.response()
		return position[0] + 1, position[1]

	def __get_cursor_iterator(self, line):
		number_of_lines = self.__buffer.get_line_count()
		if line > number_of_lines: return self.__buffer.get_start_iter()
		return self.__buffer.get_iter_at_line(line - 1)

	def __get_cursor_index(self, iterator, index):
		line_index = iterator.get_bytes_in_line()
		return line_index if index > line_index else index

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __loaded_cb(self, *args):
		from gobject import timeout_add
		timeout_add(100, self.__place_timeout)
		return False

	def __checking_cb(self, *args):
		self.__line_position = self.__get_cursor_data()
		return False
