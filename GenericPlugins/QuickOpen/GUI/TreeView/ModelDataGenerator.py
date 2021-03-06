class Generator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("filtered-files", self.__files_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		return False

	def __generate(self, files):
		self.__editor.refresh(False)
		data = [self.__split(file_data) for file_data in files]
		self.__editor.refresh(False)
		self.__manager.emit("model-data", data)
		self.__editor.refresh(False)
		return False

	def __split(self, file_data):
		_file, uri = file_data
		self.__editor.refresh(False)
		from os.path import split
		self.__editor.refresh(False)
		return split(_file)[-1], _file, uri

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __files_cb(self, manager, files):
		from gobject import idle_add
		idle_add(self.__generate, files)
		return False
