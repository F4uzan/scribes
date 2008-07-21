
# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This module documents a class that adds and removes marks in the buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Marker(object):
	"""
	This class adds and removes marks in the buffer.
	"""
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("toggle-bookmark", self.__toggle_bookmark_cb)
		self.__sigid3 = editor.connect("loaded-document", self.__restore_cb)
		self.__sigid4 = editor.connect("renamed-document", self.__restore_cb)
		self.__sigid5 = manager.connect("remove-all-bookmarks", self.__remove_bookmarks_cb)
		self.__restore_marks()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __set_properties(self):
		pixbuf = self.__create_pixbuf()
		self.__editor.textview.set_mark_category_pixbuf("scribes_bookmark", pixbuf)
		self.__editor.textview.set_mark_category_priority("scribes_bookmark", 1)
		return

	def __get_line(self, line=None):
		if line is None: return self.__editor.get_cursor_line()
		return line if self.__line_exists(line) else None

	def __create_pixbuf(self):
		from os.path import join
		current_folder = self.__editor.get_current_folder(globals())
		image_file = join(current_folder, "bookmarks.png")
		from gtk import Image
		image = Image()
		image.set_from_file(image_file)
		pixbuf = image.get_pixbuf()
		return pixbuf

	def __toggle_mark(self):
		try:
			self.__unmark() if self.__line_is_marked() else self.__mark()
		except ValueError:
			pass
		return

	def __mark(self, line=None):
		iterator = self.__iter_at_line(line)
		if iterator is None: return
		self.__editor.textbuffer.create_source_mark(None, "scribes_bookmark", iterator)
		from i18n import msg2
		message = msg2 % (self.__get_line(line) + 1)
		self.__editor.update_status_message(message, "yes")
		return

	def __unmark(self, line=None):
		iterator = self.__iter_at_line(line)
		if iterator is None: return
		end = self.__editor.forward_to_line_end(iterator.copy())
		self.__editor.textbuffer.remove_source_marks(iterator, end, "scribes_bookmark")
		from i18n import msg1
		message = msg1 % (self.__get_line(line) + 1)
		self.__editor.update_status_message(message, "yes")
		return

	def __remove_all_marks(self):
		start, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_source_marks(start, end, "scribes_bookmark")
		return

	def __restore_marks(self):
		self.__remove_all_marks()
		uri = self.__editor.uri
		if uri in (None, ""): return
		from Metadata import get_value
		lines = get_value(uri)
		if not lines: return
		mark = self.__mark
		[mark(line) for line in lines]
		return

	def __iter_at_line(self, line=None):
		get_iter = self.__editor.textbuffer.get_iter_at_line
		if line: return get_iter(line) if self.__line_exists(line) else None
		return get_iter(self.__editor.get_cursor_line())

	def __line_exists(self, line):
		iterator = self.__editor.textbuffer.get_bounds()[1]
		if line > iterator.get_line(): return False
		return True

	def __line_is_marked(self, line=None):
		line = self.__get_line()
		if line is None: raise ValueError
		marks = self.__editor.textbuffer.get_source_marks_at_line(line, "scribes_bookmark")
		if marks: return True
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggle_bookmark_cb(self, *args):
		self.__toggle_mark()
		return False

	def __restore_cb(self, *args):
		self.__restore_marks()
		return False

	def __remove_bookmarks_cb(self, *args):
		self.__remove_all_marks()
		return False