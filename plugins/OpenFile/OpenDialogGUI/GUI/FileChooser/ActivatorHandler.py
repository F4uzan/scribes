class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("open-button-activate", self.__activate_cb)
		self.__sigid3 = self.__chooser.connect("file-activated", self.__activate_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.open_gui.get_object("FileChooser")
		return

	def __update(self, uri, folders, files):
		self.__editor.response()
		is_folder = self.__editor.uri_is_folder
		folders.append(uri) if is_folder(uri) else files.append(uri)
		return False

	def __activate(self):
		try:
			self.__editor.response()
			uris = self.__chooser.get_uris()
			folders, files = [], []
			[self.__update(uri, folders, files) for uri in uris]
			if len(folders) == 1 and len(uris) == 1: raise ValueError
			if len(folders) > 0: return False
			self.__manager.emit("load-files", files)
			self.__editor.response()
		except ValueError:
			self.__manager.emit("change-folder", folders[0])
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return False
