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
This module documents a class that creates a trigger that toggles spell
checking.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	This class creates an object, a trigger, that (un)comments lines
	in several source code.
	"""

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__trigger.connect("activate", self.__toggle_comment_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = self.__create_trigger()
		self.__manager = None
		return

	def __create_trigger(self):
		"""
		Create a trigger object.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		# Trigger that (un)comments lines in several source code.
		self.__trigger = self.__editor.create_trigger("toggle_comment", "alt - c")
		self.__editor.add_trigger(self.__trigger)
		return self.__trigger

	def __toggle_comment_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		try:
			self.__manager.toggle_comment()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.toggle_comment()
		return

	def destroy(self):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the SpacesTrigger instance.
		@type self: An SpacesTrigger object.

		@param trigger: Reference to the SpacesTrigger instance.
		@type trigger: A SpacesTrigger object.
		"""
		if self.__manager: self.__manager.destroy()
		self.__editor.remove_trigger(self.__trigger)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger)
		del self
		self = None
		return