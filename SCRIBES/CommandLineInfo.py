def print_info():
	print "========================================================"
	import os
	print "System Info: ", os.uname()
	import sys
	print "Python Version: ", sys.version
	print "System Byteorder: ", sys.byteorder
	print "Python Modules: ", sys.builtin_module_names
	print "========================================================"
	from Globals import version
	print "Scribes Version: ", version
	import dbus
	print "Dbus Version: ", dbus.version
	import gtk
	print "GTK+ Version: ", gtk.gtk_version
	import gtk
	print "PyGTK Version: ",	gtk.pygtk_version
	try:
		import psyco
		print "Psyco Version: ", psyco.version_info
	except ImportError:
		print "Psyco Not Installed"
	print "========================================================"
	from Globals import dbus_iface
	services = dbus_iface.ListNames()
	service = "net.sourceforge.Scribes"
	print "Running Instance: ", services.count(service)
	print "========================================================"
	from Globals import executable_path
	from Globals import python_path, core_plugin_folder
	from Globals import data_folder
	print "Python Path: ", python_path
	print "Plugin Path: ", core_plugin_folder
	print "Data Path: ", data_folder
	print "Executable Path: ", executable_path
	print "========================================================"
	return
