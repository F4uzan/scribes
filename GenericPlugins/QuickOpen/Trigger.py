from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.TriggerManager import TriggerManager
from gettext import gettext as _

class Trigger(SignalManager, TriggerManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		TriggerManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(self.__trigger, "activate", self.__activate_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		name, shortcut, description, category = (
			"show-quick-open-window", 
			"<ctrl><alt>o", 
			_("Open files quickly"), 
			_("File Operations")
		)
		self.__trigger = self.create_trigger(name, shortcut, description, category)
		self.__manager = None
		return

	def destroy(self):
		self.disconnect()
		self.remove_triggers()
		if self.__manager: self.__manager.destroy()
		del self
		return False

	def __get_manager(self):
		if self.__manager: return self.__manager
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return self.__manager

	def __activate(self):
		self.__get_manager().show()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate)
		return
