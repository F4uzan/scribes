class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger.connect("activate", self.__show_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		from Manager import Manager
		self.__manager = Manager(editor)
		from MenuItem import MenuItem
		self.__menuitem = MenuItem(editor)
		self.__trigger = self.__create_trigger()
		return

	def __create_trigger(self):
		# Trigger to show the automatic replacement dialog.
		trigger = self.__editor.create_trigger("show_autoreplace_dialog")
		self.__editor.add_trigger(trigger)
		return trigger

	def __show_cb(self, *args):
		self.__manager.show()
		return

	def destroy(self):
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger)
		self.__menuitem.destroy()
		self.__manager.destroy()
		del self
		self = None
		return