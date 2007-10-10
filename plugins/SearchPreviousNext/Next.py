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
This module documents a class that creates an object that searches for
text in the text editor's buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class SearchNext(object):
	"""
	This class implements an object that searches for a text in the
	text editor's buffer without showing the any search interfaces. The
	text to be searched is determined by the last query in the search
	and replace manager.
	"""

	def __init__(self, trigger, editor):
		"""
		Initialize the object.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.

		@param trigger: A trigger to activate searching.
		@type trigger: A Trigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.trigger("initialize_search_replace_manager")
		self.__init_attributes(editor)
		self.__signal_id_1 = editor.textview.connect("button-press-event", self.__button_press_event_cb)
		self.__signal_id_2 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_3 = editor.textbuffer.connect("insert-text", self.__insert_text_cb)
		self.__signal_id_4 = trigger.connect("destroy", self.__destroy_cb)
		self.__block_signals()

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__search_replace_manager = editor.get_object("SearchReplaceManager")
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_is_blocked = False
		return

	def next(self):
		"""
		Search for text in the buffer.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.
		"""
		if not self.__search_replace_manager.queries:
			self.__editor.trigger("show_findbar")
			return
		if self.__signal_is_blocked:
			self.__unblock_signals()
		if self.__search_replace_manager.index is None:
			string = self.__search_replace_manager.queries[-1]
			start, end = self.__editor.textbuffer.get_bounds()
			start = self.__editor.get_cursor_position()
			bmark = self.__editor.textbuffer.create_mark(None, start, True)
			emark = self.__editor.textbuffer.create_mark(None, end, False)
			self.__search_replace_manager.find(string, bmark, emark)
			return
		self.__search_replace_manager.next()
		return

	def __button_press_event_cb(self, textview, event):
		"""
		Handles callback when the "button-press-event" is emitted.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.

		@param textview: The text editor's view.
		@type textview: A ScribesTextView object.

		@param event: An event that happens when the mouse buttons are pressed.
		@type event: An Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__block_signals()
		self.__search_replace_manager.enable_incremental_searching(False)
		self.__search_replace_manager.reset()
		return False

	def __insert_text_cb(self, *args):
		"""
		Handles callback when the "insert-text" signal is emitted.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.

		@param *args: The callback arguments.
		@type *args: A List object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__block_signals()
		self.__search_replace_manager.enable_incremental_searching(False)
		self.__search_replace_manager.reset()
		return False

	def __key_press_event_cb(self, textview, event):
		"""
		Handles callback when the "key-press-event" is emitted.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.

		@param textview: The text editor's view.
		@type textview: A ScribesTextView object.

		@param event: An event that happens when the mouse buttons are pressed.
		@type event: An Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk.gdk import keyval_name
		if keyval_name(event.keyval) in ["Escape"]:
			self.__block_signals()
			self.__search_replace_manager.enable_incremental_searching(False)
			self.__search_replace_manager.reset()
		return False

	def __block_signals(self):
		"""
		Block signals associated with this object.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.
		"""
		self.__editor.textview.handler_block(self.__signal_id_1)
		self.__editor.textview.handler_block(self.__signal_id_2)
		self.__editor.textbuffer.handler_block(self.__signal_id_3)
		self.__signal_is_blocked = True
		return

	def __unblock_signals(self):
		"""
		Unblock signals associated with this object.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.
		"""
		self.__editor.textview.handler_unblock(self.__signal_id_1)
		self.__editor.textview.handler_unblock(self.__signal_id_2)
		self.__editor.textbuffer.handler_unblock(self.__signal_id_3)
		self.__signal_is_blocked = False
		return

	def __destroy_cb(self, trigger):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the SearchNext instance.
		@type self: A SearchNext object.

		@param trigger: Trigger to activate searching.
		@type trigger: A Trigger object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__signal_id_4, trigger)
		self = None
		del self
		return
