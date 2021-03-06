class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__set()
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.data_folder, "Editor.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set(self):
		self.__editor.set_data("gui", self.__glade)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
