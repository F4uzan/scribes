class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__activate_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__activate_cb)
		self.__sigid3 = self.__trigger3.connect("activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger1 = self.__create_trigger("scroll_up", "<ctrl>Up")
		self.__trigger2 = self.__create_trigger("scroll_down", "<ctrl>Down")
		self.__trigger3 = self.__create_trigger("center", "<alt>m")
		return

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger3)
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3)
		self.__editor.remove_triggers(triggers)
		del self
		self = None
		return False

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __get_manager(self):
		from Manager import Manager
		return Manager(self.__editor)

	def __activate_cb(self, trigger):
		if not self.__manager: self.__manager = self.__get_manager()
		function = {
			self.__trigger1: self.__manager.scroll_up,
			self.__trigger2: self.__manager.scroll_down,
			self.__trigger3: self.__manager.center,
		}
		function[trigger]()
		return

	def destroy(self):
		self.__destroy()
		return
