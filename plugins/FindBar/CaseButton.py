# -*- coding: utf-8 -*-
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
This module exposes a class that creates the text editor's findbar's case
check button.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import CheckButton

class FindCaseButton(CheckButton):
	"""
	This class creates a check button for the text editor's findbar. The class
	defines the behavior and default properties of the check button.
	"""

	def __init__(self, findbar):
		"""
		Initialize the check button.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		from i18n import msg0001
		CheckButton.__init__(self, msg0001, use_underline=True)
		self.__init_attributes(findbar)
		self.__signal_id_7 = self.connect("toggled", self.__casebutton_toggled_cb)
		self.__signal_id_1 = self.__editor.connect("show-bar", self.__casebutton_show_bar_cb)
		self.__signal_id_2 = self.__searchmanager.connect("searching", self.__casebutton_searching_cb)
		self.__signal_id_3 = self.__searchmanager.connect("matches-found", self.__casebutton_matches_found_cb)
		self.__signal_id_4 = self.__searchmanager.connect("no-matches-found", self.__casebutton_no_matches_found_cb)
		self.__signal_id_5 = self.__searchmanager.connect("cancel", self.__casebutton_cancel_cb)
		self.__signal_id_6 = findbar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, findbar):
		"""
		Initialize the check button's attributes.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		self.__editor = findbar.editor
		self.__searchmanager = findbar.search_replace_manager
		from gconf import client_get_default
		self.__client = client_get_default()
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = None
		return

	def __casebutton_toggled_cb(self, togglebutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param togglebutton: The findbar's case check button.
		@type togglebutton: A CheckButton object.
		"""
		self.__searchmanager.reset()
		value = self.get_property("active")
		self.__client.set_bool("/apps/scribes/match_case", value)
		self.__client.notify("/apps/scribes/match_case")
		return True

	def __casebutton_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: One of the text editor's bars.
		@type bar: A ScribesBar object.
		"""
		self.set_property("sensitive", True)
		value = self.__client.get_bool("/apps/scribes/match_case")
		if not self.get_property("active") is value:
			self.set_property("active", value)
		return

	def __casebutton_searching_cb(self, searchmanager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __casebutton_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __casebutton_no_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __casebutton_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __destroy_cb(self, findbar):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the FindCaseButton instance.
		@type self: A FindCaseButton object.

		@param findbar: Reference the Findbar instance.
		@type findbar: A Findbar object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_6, findbar)
		self.__editor.disconnect_signal(self.__signal_id_7, self)
		self.destroy()
		del self
		self = None
		return
