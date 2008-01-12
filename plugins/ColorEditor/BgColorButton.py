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
This module documents a class that creates the foreground color button
for the text editor's color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ColorButton

class BackgroundButton(ColorButton):
	"""
	This class creates a color button for the text editor's color
	editor. The color button allows users to set the foreground color of
	text editor's buffer.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the button.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ColorButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.connect("color-set", self.__color_set_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__theme_database_uri, MONITOR_FILE,
					self.__use_theme_colors_cb)
		self.__monitor_id_2 = monitor_add(self.__bg_database_uri, MONITOR_FILE,
					self.__bgcolor_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		theme_database_path = join(preference_folder, "UseTheme.gdb")
		bg_database_path = join(preference_folder, "BackgroundColor.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__theme_database_uri = get_uri_from_local_path(theme_database_path)
		self.__bg_database_uri = get_uri_from_local_path(bg_database_path)
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		from BackgroundColorMetadata import get_value
		bgcolor = get_value()
		from gtk.gdk import color_parse
		bgcolor = color_parse(bgcolor)
		self.set_color(bgcolor)
		from i18n import msg0011
		self.set_title(msg0011)
		from SCRIBES.tooltips import background_button_tip
		self.__editor.tip.set_tip(self, background_button_tip)
		from UseThemeMetadata import get_value
		use_theme_colors = get_value()
		self.set_property("sensitive", not use_theme_colors)
		return

	def __bgcolor_cb(self, *args):
		"""
		Handles callback when foreground color changes.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		color = self.get_color()
		color = self.__editor.convert_color_to_string(color)
		from operator import eq
		from BackgroundColorMetadata import get_value
		bgcolor = get_value()
		if eq(bgcolor, color): return
		from gtk.gdk import color_parse
		self.set_color(color_parse(bgcolor))
		return

	def __color_set_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		bgcolor = self.get_color()
		bgcolor = self.__editor.convert_color_to_string(bgcolor)
		from BackgroundColorMetadata import set_value
		set_value(bgcolor)
		return True

	def __use_theme_colors_cb(self, *args):
		"""
		Handles callback when foreground color changes.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		from UseThemeMetadata import get_value
		use_theme_colors = get_value()
		if use_theme_colors:
			if self.get_property("sensitive"):
				self.set_property("sensitive", False)
		else:
			from operator import not_
			if not_(self.get_property("sensitive")):
				self.set_property("sensitive", True)
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param manager: Reference to the ColorEditorManager instance.
		@type manager: A ColorEditorManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		if self.__monitor_id_2: monitor_cancel(self.__monitor_id_2)
		del self
		self = None
		return
