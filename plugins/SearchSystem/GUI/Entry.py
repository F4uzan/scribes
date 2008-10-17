class Entry(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-bar", self.__show_cb)
		self.__sigid3 = self.__entry.connect("changed", self.__changed_cb)
		self.__sigid4 = self.__entry.connect("activate", self.__activate_cb)
		self.__sigid5 = self.__entry.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid6 = self.__manager.connect("focus-entry", self.__focus_entry_cb)
		self.__entry.props.sensitive = True
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.gui.get_widget("Entry")
		return  
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__entry)
		self.__editor.disconnect_signal(self.__sigid4, self.__entry)
		self.__editor.disconnect_signal(self.__sigid5, self.__entry)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__entry.destroy()
		del self
		self = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __show_cb(self, *args):
		self.__entry.grab_focus()
		return False
	
	def __changed_cb(self, *args):
		text = self.__entry.get_text()
		self.__manager.emit("search-string", text)
		return False
	
	def __activate_cb(self, *args):
		if not self.__entry.get_text(): return False
		self.__manager.emit("search")
		return False

	def __key_press_event_cb(self, entry, event):
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide-bar")
		return False

	def __focus_entry_cb(self, *args):
		self.__entry.grab_focus()
		return False