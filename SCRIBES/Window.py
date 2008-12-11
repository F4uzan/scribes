﻿# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module implements a class responsible for creating a window object for
text editor instances.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gettext import gettext as _

class Window(object):
	"""
	This class defines the behavior of the window for the text editor.
	"""

	def __init__(self, editor, uri):
		self.__init_attributes(editor, uri)
		self.__set_properties()
		self.__sigid1 = self.__window.connect("delete-event", self.__delete_event_cb)
#		self.__sigid2 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid3 = editor.connect("close", self.__close_cb)
		self.__sigid4 = self.__window.connect("window-state-event", self.__state_event_cb)
		self.__sigid5 = self.__window.connect("focus-out-event", self.__focus_out_event_cb)
		self.__sigid6 = self.__window.connect("focus-in-event", self.__focus_in_event_cb)
		self.__sigid7 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid8 = editor.connect("loaded-file", self.__loaded_file_cb)
		self.__sigid9 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid10 = editor.connect("modified-file", self.__modified_file_cb)
		self.__sigid11 = editor.connect("readonly", self.__readonly_cb)
		self.__sigid12 = self.__window.connect_after("focus-out-event", self.__focus_out_after_event_cb)
		self.__sigid13 = editor.connect("renamed-file", self.__renamed_file_cb)
		self.__sigid14 = editor.connect("bar-is-active", self.__active_cb)
		self.__sigid15 = editor.connect("fullscreen", self.__fullscreen_cb)
		editor.register_object(self)
		self.__position_window()
		editor.response()
		self.__window.set_property("sensitive", True)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__window = editor.gui.get_widget("Window")
		self.__uri = str(uri) if uri else None
		self.__title = self.__set_title()
		self.__is_minimized = False
		self.__is_maximized = False
		self.__positioned = False
		self.__bar_is_active = False
		return

	def __destroy(self):
		self.__editor.response()
		self.__window.hide()
		self.__editor.response()
		self.__editor.disconnect_signal(self.__sigid1, self.__window)
#		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__editor.disconnect_signal(self.__sigid6, self.__window)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor)
		self.__editor.disconnect_signal(self.__sigid11, self.__editor)
		self.__editor.disconnect_signal(self.__sigid12, self.__editor)
		self.__editor.disconnect_signal(self.__sigid13, self.__editor)
		self.__editor.disconnect_signal(self.__sigid14, self.__editor)
		self.__editor.disconnect_signal(self.__sigid15, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		# Add new signal to window.
		from gobject import signal_new, signal_query, SIGNAL_RUN_LAST
		from gobject import TYPE_STRING, TYPE_BOOLEAN, SIGNAL_ACTION
		from gobject import SIGNAL_NO_RECURSE, type_register
		SIGNAL = SIGNAL_ACTION|SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE
		from gtk import Window
		if signal_query("scribes-key-event", Window) is None:
			signal_new("scribes-key-event", Window, SIGNAL_ACTION, None, ())
			signal_new("scribes-close-window", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
			signal_new("scribes-close-window-nosave", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
			signal_new("shutdown", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
			signal_new("fullscreen", Window, SIGNAL, TYPE_BOOLEAN, (TYPE_STRING,))
			type_register(type(self.__window))
		from gtk import AccelGroup
		self.__window.add_accel_group(AccelGroup())
		from gtk.gdk import KEY_PRESS_MASK
		self.__window.add_events(KEY_PRESS_MASK)
		width, height = self.__editor.calculate_resolution_independence(self.__window, 1.462857143, 1.536)
		self.__window.set_property("default-height", height)
		self.__window.set_property("default-width", width)
		if self.__uri: self.__update_window_title(_('Loading "%s" ...') % self.__title)
		return

	def __update_window_title(self, title):
		self.__window.set_property("title", title)
		self.__window.set_data("minimized", self.__is_minimized)
		self.__window.set_data("maximized", self.__is_maximized)
		return False

	def __set_title(self):
		from gnomevfs import URI
		return URI(self.__uri).short_name.encode("utf-8") if self.__uri else _("Unsaved Document")

	def __set_readonly(self, readonly):
		title = self.__set_title()
		update = self.__update_window_title
		update("%s [READONLY]" % title) if readonly else update(title)
		return False

	def __position_window(self):
		try:
			self.__window.hide()
			uri = self.__uri if self.__uri else "<EMPTY>"
			if uri != "<EMPTY>": self.__positioned = True
			# Get window position from the position database, if possible.
			from PositionMetadata import get_window_position_from_database
			maximize, width, height, xcoordinate, ycoordinate = \
				get_window_position_from_database(uri)# or \
			if maximize:
				self.__window.maximize()
			else:
				self.__window.resize(width, height)
				self.__window.move(xcoordinate, ycoordinate)
		except TypeError:
			pass
		finally:
			self.__window.present()
		return False

	def __set_window_position_in_database(self):
		xcoordinate, ycoordinate = self.__window.get_position()
		width, height = self.__window.get_size()
		is_maximized = self.__is_maximized
		uri = self.__uri if self.__uri else "<EMPTY>"
		window_position = (True, None, None, None, None) if is_maximized else (False, width, height, xcoordinate, ycoordinate)
		from PositionMetadata import update_window_position_in_database
		update_window_position_in_database(str(uri), window_position)
		return

	def __precompile_methods(self):
		methods = (self.__key_press_event_cb, self.__focus_in_event_cb,
			self.__focus_out_event_cb, self.__focus_out_after_event_cb,
			self.__state_event_cb, self.__modified_file_cb)
		self.__editor.optimize(methods)
		return False

########################################################################
#
#					Signal and Event Callback Handlers
#
########################################################################

	def __delete_event_cb(self, widget, event):
		self.__editor.close()
		return True

	def __checking_file_cb(self, editor, uri):
		self.__uri = uri
		if not self.__positioned: self.__position_window()
		self.__title = self.__set_title()
		self.__update_window_title(_('Loading "%s" ...') % self.__title)
		return False

	def __loaded_file_cb(self, *args):
		self.__title = self.__set_title()
		readonly = self.__editor.readonly
		self.__set_readonly(readonly) if readonly else self.__update_window_title(self.__title)
		return False

	def __load_error_cb(self, *args):
		self.__uri = None
		self.__title = self.__set_title()
		self.__update_window_title(self.__title)
		self.__position_window()
		self.__window.present()
		return False

	def __modified_file_cb(self, editor, modified):
		title = str(self.__editor.uri_object.short_name) if self.__editor.uri else _("Unsaved Document")
		set_title = self.__window.set_title
		set_title("*%s" % title) if modified else set_title(title)
		return False

	def __focus_out_after_event_cb(self, *args):
		self.__editor.emit("window-focus-out")
		return False

	def __focus_out_event_cb(self, window, event):
		# Save a document when the text editor's window loses focus.
#		if self.__editor.uri and self.__editor.file_is_saved is False and self.__editor.is_readonly is False:
#			self.__editor.save_file()
#		if self.__is_quiting: return False
		self.__window.grab_remove()
		self.__set_window_position_in_database()
		return False

	def __focus_in_event_cb(self, *args):
		self.__window.grab_add()
		self.__set_window_position_in_database()
		return False

	def __state_event_cb(self, window, event):
		from gtk.gdk import WINDOW_STATE_MAXIMIZED, WINDOW_STATE_FULLSCREEN
		from gtk.gdk import WINDOW_STATE_ICONIFIED
		state = event.new_window_state
		MINIMIZED = state & WINDOW_STATE_ICONIFIED
		MAXIMIZED = (state & WINDOW_STATE_MAXIMIZED) or (state & WINDOW_STATE_FULLSCREEN)
		self.__is_minimized = True if MINIMIZED else False
		self.__is_maximized = True if MAXIMIZED else False
		return False

	def __readonly_cb(self, editor, readonly):
		self.__set_readonly(readonly)
		return False

	def __renamed_file_cb(self, editor, uri, *args):
		from gnomevfs import URI
		self.__window.set_title(URI(uri).short_name)
		return False

	def __key_press_event_cb(self, window, event):
		return False

	def __close_cb(self, editor, save_file):
		if save_file: self.__set_window_position_in_database()
		self.__destroy()
		return False

	def __active_cb(self, editor, active):
		self.__bar_is_active = active
		return False

	def __fullscreen_cb(self, manager, fullscreen):
		self.__editor.response()
		self.__window.fullscreen() if fullscreen else self.__window.unfullscreen()
		self.__editor.response()
		return True
