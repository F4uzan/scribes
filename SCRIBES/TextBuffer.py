﻿# -*- coding: utf-8 -*-
# Copyright (C) 2005 Lateef Alabi-Oki
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
This module implements a class that creates the buffer for the text
editor.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtksourceview import SourceBuffer

class ScribesTextBuffer(SourceBuffer):
	"""
	This class creates the buffer for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to a ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		SourceBuffer.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_2 = editor.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_3 = editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_4 = editor.connect("load-error", self.__load_error_cb)
		self.__signal_id_5 = editor.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_6 = editor.connect("enable-readonly", self.__enable_readonly_cb)
		self.__signal_id_7 = editor.connect("disable-readonly", self.__disable_readonly_cb)
		self.__signal_id_8 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_9 = editor.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_10 = self.connect("notify::cursor-position", self.__cursor_position_cb)
		self.__signal_id_11 = editor.connect("reload-document", self.__reload_document_cb)
		self.__signal_id_12 = self.connect_after("notify::cursor-position", self.__cursor_position_after_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the attributes of the text editor's buffer.

		This function contains some attributes not available in the
		gtksourceview.SourceBuffer class. The attributes provided solely for
		purpose of the text editor.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__uri = None
		# Register a unique number with the editor's termination queue
		self.__termination_id = editor.register_object()
		self.__undoable_action = False
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = None
		return

	def __set_properties(self):
		"""
		Set the editor's buffer properties.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.
		"""
		self.notify("cursor-position")
		self.set_check_brackets(False)
		self.set_max_undo_levels(0)
		self.set_text("")
		self.set_modified(False)
		return

################################################################################
#
#							Signal Handlers
#
################################################################################

	def __checking_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor is in the process of loading a
		document into the text editor's buffer.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: An instance of the text editor's.
		@type editor: An Editor object.
		"""
		self.__uri = uri
		self.begin_not_undoable_action()
		self.__undoable_action = True
		from gobject import idle_add
		idle_add(self.__activate_sytnax_colors)
		return

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor has finished loading documents
		into the text editor's buffer.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_modified(False)
		self.end_not_undoable_action()
		self.__undoable_action = False
		self.__set_cursor_positon()
		return

	def __saved_document_cb(self, editor, uri):
		"""
		Handles callback when the text editor's buffer has finished saving the
		contents of the text editor's buffer.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: An instance of the text editor's.
		@type editor: An Editor object.
		"""
		self.set_modified(False)
		return

	def __enable_readonly_cb(self, editor):
		"""
		Handles callback when the text editor is switched to readonly mode.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_check_brackets(False)
		return

	def __disable_readonly_cb(self, editor):
		"""
		Handles callback when the text editor is switched from readonly to
		readwrite mode.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: An instance of the text editor.
		@type editor: An Editor object.
		"""
		self.set_check_brackets(True)
		return

	def __load_error_cb(self, editor, uri):
		"""
		Handles callback when the text editor fails to load a document.

		This function resets the buffer to a usable state.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: An instance of the text editor
		@type editor: An Editor object.
		"""
		self.__uri = None
		if self.__undoable_action: self.end_not_undoable_action()
		self.__set_properties()
		return

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "quit" signal is emitted.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import idle_add
		idle_add(self.__update_cursor_metadata, self.__uri)
		return

	def __close_document_no_save_cb(self, editor):
		self.__destroy()
		return

	def __renamed_document_cb(self, editor, uri):
		"""
		Handles callback when the name of the document is renamed.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__uri = uri
		self.__activate_sytnax_colors()
		self.set_modified(False)
		self.set_check_brackets(True)
		return

	def __reload_document_cb(self, *args):
		self.set_modified(False)
		self.set_text("")
		self.set_modified(False)
		return

	def __cursor_position_cb(self, *args):
		self.__editor.emit("cursor-moved")
		self.__make_responsive()
		return False

	def __cursor_position_after_cb(self, *args):
		self.__make_responsive()
		return False

	def __make_responsive(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__cursor_id)
		except:
			pass
		self.__cursor_id = idle_add(self.__test_response)
		return False

	def __test_response(self):
		self.__editor.response()
		return False

########################################################################
#
#						Helper Methods
#
########################################################################

	def __activate_sytnax_colors(self):
		"""
		Activate syntax highlight colors for the text editor's buffer.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		# Activate syntax highlight for the language.
		from syntax import activate_syntax_highlight
		activate_syntax_highlight(self, self.__editor.language)
		return False

	def __update_cursor_metadata(self, uri):
		"""
		Update the cursor database with information about the cursor position in
		the text editor's buffer.

		@param self: Reference to the ScribesWindow instance.
		@type self: A ScribesWindow object.

		@param uri: A universal resource identifier representing, or pointing
			to, a text document.
		@type uri: A String object.
		"""
		if self.__uri:
			from cursor_metadata import update_cursor_position_in_database
			from cursor import get_cursor_line, get_cursor_index
			cursor_line = get_cursor_line(self)
			cursor_index = get_cursor_index(self)
			cursor_position = cursor_line, cursor_index
			update_cursor_position_in_database(uri, cursor_position)
		self.__destroy()
		return False

	def __set_cursor_positon(self):
		"""
		Determine where to place the cursor when a file is loaded.

		The editor stores the last cursor position in a database so that
		when a file is loaded the cursor is placed at the last position in the
		file.

		However, it is possible that another software program alters the state
		of the file. Thus making the information in the editor's database
		obsolete. In such a case, the editor tries to determine where to place
		the cursor.

		If the changes are too drastic, the editor places the cursor at the
		begining of the file. If the changes are minor, the editor places the
		cursor at an approximate position close the the last position the cursor
		was last seen.

		@param self: Reference to the Loader object.
		@type self: A Loader object.
		"""
		self.__editor.response()
		try:
			from cursor_metadata import get_cursor_position_from_database
			position = get_cursor_position_from_database(self.__uri)
			cursor_line, cursor_index = position[0] + 1, position[1]
		except TypeError:
			cursor_line, cursor_index = 1, 0
		start_iterator = self.get_start_iter()
		number_of_lines = self.get_line_count()
		from operator import gt
		if gt(cursor_line, number_of_lines):
			self.place_cursor(start_iterator)
			self.__editor.response()
			return False
		iterator = self.get_iter_at_line(cursor_line - 1)
		line_index = iterator.get_bytes_in_line()
		if gt(cursor_index, line_index):
			iterator.set_line_index(line_index)
		else:
			iterator.set_line_index(cursor_index)
		self.place_cursor(iterator)
		from cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		self.__editor.response()
		return False

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__make_responsive)
#			bind(self.__set_cursor_positon)
#			bind(self.__update_cursor_metadata)
#			bind(self.__activate_sytnax_colors)
		except ImportError:
			pass
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_10, self)
		self.__editor.disconnect_signal(self.__signal_id_11, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_12, self)
		self.__editor.unregister_object(self.__termination_id)
		del self
		self = None
		return False
