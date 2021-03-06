from SCRIBES.SignalConnectionManager import SignalManager

class Positioner(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "single-line-boundary", self.__boundary_cb)
		self.connect(manager, "processed-text", self.__processed_cb)
		self.connect(manager, "inserted-text", self.__text_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__selection = False
		self.__buffer = editor.textbuffer
		self.__offset = 0
		self.__boundaries = ()
		self.__commenting = False
		self.__old_text = ""
		self.__new_text = ""
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __iter_after_indent(self):
		iterator = self.__buffer.get_iter_at_mark(self.__boundaries[0])
		iterator = self.__editor.backward_to_line_begin(iterator)
		while iterator.get_char() in (" ", "\t"): iterator.forward_char()
		return iterator

	def __iter_at(self, offset):
		iterator = self.__buffer.get_iter_at_offset(offset)
		return iterator

	def __position(self):
		# Ignore multiline text.
		if self.__selection: return False
		if not self.__boundaries: return False
		if len(self.__new_text.splitlines()) > 1: return False
		# Adjust new cursor position based on whether comment string 
		# was added or removed.
		offset = self.__offset + len(self.__new_text) - len(self.__old_text)
		# Always ensure that cursor is placed somewhere on the current
		# line. If all else fails place cursor at the beginning of 
		# indentation.
		start_offset = self.__buffer.get_iter_at_mark(self.__boundaries[0]).get_offset()
		iterator = self.__iter_after_indent() if offset < start_offset else self.__iter_at(offset)
		self.__buffer.place_cursor(iterator)
		self.__manager.emit("finished")
		self.__boundaries = ()
		self.__old_text = ""
		self.__new_text = ""
		return False

	def __update_old_text(self, boundaries):
		start = self.__buffer.get_iter_at_mark(boundaries[0])
		end = self.__buffer.get_iter_at_mark(boundaries[1])
		self.__old_text = self.__buffer.get_text(start, end)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundaries):
		self.__boundaries = boundaries
		self.__update_old_text(boundaries)
		return False

	def __activate_cb(self, *args):
		self.__selection = self.__editor.has_selection
		self.__offset = self.__editor.cursor.get_offset()
		return False

	def __text_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__position)
		return False

	def __processed_cb(self, manager, text):
		self.__new_text = text
		return False
