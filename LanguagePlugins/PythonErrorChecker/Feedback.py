from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "error-data", self.__message_cb)
		self.connect(manager, "remote-file-message", self.__error_cb)
		self.connect(manager, "check-message", self.__check_cb)
		self.connect(manager, "error-check-type", self.__type_cb, True)
		self.connect(manager, "toggle-error-check", self.__toggle_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__message = ""
		self.__editor = editor
		self.__is_first_time = True
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __message_cb(self, manager, data):
		if data[0]:
			message = "Error: %s on line %s" % (data[1], data[0])
			if self.__message == message: return False
			self.__message = message
			self.__editor.set_message(message, "error")
		else:
			message = _("No errors found")
			self.__editor.update_message(message, "yes")
			self.__editor.unset_message(self.__message, "error")
			self.__message = ""
		return False

	def __error_cb(self, *args):
		message = _("No error checking on remote file")
		self.__editor.update_message(message, "no", 3)
		return False

	def __check_cb(self, *args):
		message = _("checking for errors please wait...")
		self.__editor.update_message(message, "run", 60)
		return False

	def __type_cb(self, manager, more_error_checks):
		from Exceptions import FirstTimeError
		try:
			if self.__is_first_time: raise FirstTimeError
			message = _("Switched to Python error checking") if more_error_checks else _("Switched to syntax error checking")
			self.__editor.hide_message()
			self.__editor.update_message(message, "yes")
		except FirstTimeError:
			self.__is_first_time = False
		return False

	def __toggle_cb(self, *args):
		message = _("switching please wait...")
		self.__editor.update_message(message, "run", 20)
		return False
