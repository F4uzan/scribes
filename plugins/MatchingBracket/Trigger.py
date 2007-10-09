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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that creates a trigger to jump to matching
pair characters.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class MatchingBracketTrigger(GObject):
	"""
	This class implements an object that finds matching pair characters.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the trigger object.

		@param self: Reference to the MatchingBracketTrigger instance.
		@type self: A MatchingBracketTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__find_matching_bracket_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)


	def __init_attributes(self, editor):
		"""
		Initialize the object's data attributes.

		@param self: Reference to the MatchingBracketTrigger instance.
		@type self: A MatchingBracketTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __create_trigger(self):
		"""
		Create a trigger to find matching brackets.

		@param self: Reference to the MatchingBracketTrigger instance.
		@type self: A MatchingBracketTrigger object.
		"""
		self.__trigger = self.__editor.create_trigger("find_matching_bracket", "alt - B")
		self.__editor.add_trigger(self.__trigger)
		return

	def __find_matching_bracket_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the MatchingBracketTrigger instance.
		@type self: A MatchingBracketTrigger object.

		@param trigger: An object that finds matching brackets.
		@type trigger: A Trigger object.
		"""
		result = self.__find_matching_bracket()
		if result:
			iterator = self.__editor.get_cursor_iterator()
			line = iterator.get_line() + 1
			from i18n import msg0001
			message = msg0001 % (line)
			self.__editor.feedback.update_status_message(message, "suceed")
		else:
			from i18n import msg0002
			self.__editor.feedback.update_status_message(msg0002, "fail")
		return

	def __find_matching_bracket(self):
		"""
		Find matching bracket, if any.

		@param self: Reference to the MatchingBracketTrigger instance.
		@type self: A MatchingBracketTrigger object.

		@return: True if a matching bracket was found.
		@rtype: A Boolean object.
		"""
		from gtksourceview import source_iter_find_matching_bracket as match
		iterator = self.__editor.get_cursor_iterator()
		if match(iterator):
			self.__editor.textbuffer.place_cursor(iterator)
			self.__editor.move_view_to_cursor()
			return True
		return False

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AboutTrigger instance.
		@type self: An AboutTrigger object.

		@param trigger: Reference to the AboutTrigger instance.
		@type trigger: An AboutTrigger object.
		"""
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		del self
		self = None
		return
