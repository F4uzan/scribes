# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that creates a trigger to close a Scribes
window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class CloseWindowTrigger(GObject):
	"""
	This class creates an object, a trigger, that allows users to close
	a Scribes window.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the CloseWindowTrigger instance.
		@type self: A CloseWindowTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__close_window_trigger.connect("activate", self.__close_window_cb)
		self.__signal_id_3 = self.__close_all_windows_trigger.connect("activate", self.__close_all_windows_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the CloseWindowTrigger instance.
		@type self: A CloseWindowTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__close_window_trigger = None
		self.__close_all_windows_trigger = None
		self.__signal_id_2 = None
		self.__signal_id_1 = None
		self.__signal_id_3 = None
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the CloseWindowTrigger instance.
		@type self: A CloseWindowTrigger object.
		"""
		# Trigger to close a Scribes window.
		self.__close_window_trigger = self.__editor.create_trigger("close_window", "ctrl - w")
		self.__editor.add_trigger(self.__close_window_trigger)

		# Trigger to close all Scribes windows.
		self.__close_all_windows_trigger = self.__editor.create_trigger("close_all_windows", "ctrl - Q")
		self.__editor.add_trigger(self.__close_all_windows_trigger)
		return

	def __close_window_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CloseWindowTrigger instance.
		@type self: A CloseWindowTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		self.__editor.emit("close-document")
		return

	def __close_all_windows_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CloseWindowTrigger instance.
		@type self: A CloseWindowTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		self.__editor.instance_manager.close_all_windows()
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the CloseWindowTrigger instance.
		@type self: An CloseWindowTrigger object.

		@param trigger: Reference to the CloseWindowTrigger instance.
		@type trigger: A CloseWindowTrigger object.
		"""
		self.__editor.remove_trigger(self.__close_window_trigger)
		self.__editor.remove_trigger(self.__close_all_windows_trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__close_window_trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__close_all_windows_trigger)
		del self
		self = None
		return
