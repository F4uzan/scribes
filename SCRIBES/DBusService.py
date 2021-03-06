from dbus.service import Object, method, BusName

class DBusService(Object):

	def __init__(self, manager):
		from Globals import session_bus
		from dbus.exceptions import NameExistsException
		try:
			service_name = "net.sourceforge.Scribes"
			object_path = "/net/sourceforge/Scribes"
			bus_name = BusName(service_name, bus=session_bus, do_not_queue=True)
			Object.__init__(self, bus_name, object_path)
			self.__manager = manager
		except NameExistsException:
			print "ERROR! Another instances of Scribes is already running. Cannot run more than one instance of Scribes. Killing this instance!"
			manager.force_quit()

	@method("net.sourceforge.Scribes")
	def open_window(self):
		from gobject import idle_add
		return idle_add(self.__manager.open_window)

	@method("net.sourceforge.Scribes", in_signature="asss")
	def open_files(self, uris, encoding="utf-8", stdin=""):
		uris = uris if uris else None
		stdin = stdin if stdin else None
		from gobject import idle_add
		return idle_add(self.__manager.open_files, uris, encoding, stdin)

	@method("net.sourceforge.Scribes", out_signature="as")
	def get_uris(self):
		return self.__manager.get_uris()

	@method("net.sourceforge.Scribes", out_signature="as")
	def get_text(self):
		return self.__manager.get_text()
