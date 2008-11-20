class TreeView(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("dictionary", self.__dictionary_cb)
		self.__sigid3 = self.__treeview.connect("cursor-changed", self.__changed_cb)
		self.__sigid4 = self.__abvrenderer.connect("edited", self.__abvedited_cb)
		self.__sigid5 = self.__rplrenderer.connect("edited", self.__rpledited_cb)
		self.__sigid6 = self.__model.connect("row-changed", self.__row_changed_cb)
		self.__block_row_changed_signal()
		self.__sigid7 = manager.connect("show-window", self.__show_cb)
		self.__sigid8 = manager.connect("hide-window", self.__hide_cb)
		self.__sigid9 = self.__treeview.connect("key-press-event", self.__event_cb)
		self.__sigid10 = manager.connect("add-row", self.__add_row_cb)
		self.__sigid11 = manager.connect("edit-row", self.__edit_row_cb)
		self.__sigid12 = manager.connect("delete-row", self.__delete_row_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__model = self.__create_model()
		self.__treeview = manager.gui.get_widget("TreeView")
		self.__abvrenderer = self.__create_renderer()
		self.__rplrenderer = self.__create_renderer()
		self.__abvcolumn = self.__create_abbreviation_column()
		self.__rplcolumn = self.__create_replacement_column()
		self.__string = None
		self.__update = True
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, self.__abvrenderer)
		self.__editor.disconnect_signal(self.__sigid5, self.__rplrenderer)
		self.__editor.disconnect_signal(self.__sigid6, self.__model)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		self.__editor.disconnect_signal(self.__sigid9, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid10, self.__manager)
		self.__editor.disconnect_signal(self.__sigid11, self.__manager)
		self.__editor.disconnect_signal(self.__sigid12, self.__manager)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __get_string(self, path, column):
		iterator = self.__model.get_iter(path)
		return self.__model.get_value(iterator, column)

	def __exists(self, text):
		for row in self.__model:
			if text == self.__model.get_value(row.iter, 0) : return True
		return False

	def __validate(self, text):
		message = None
		from gettext import gettext as _
		if not text: message = _("Abbreviation must contain text")
		if text in (" ", "\t"): message = _("Invalid abbreviation")
		if " " in text: message = _("Abbreviation must not contain whitespace")
		if "\t" in text: message = _("Abbreviation must not be space")
		if self.__exists(text): message = _("%s already exists") % text
		if message is None: return False
		print message
		raise ValueError
		return False

	def __block_row_changed_signal(self):
		self.__model.handler_block(self.__sigid6)
		return False

	def __unblock_row_changed_signal(self):
		self.__model.handler_unblock(self.__sigid6)
		return False

	def __process_abvrenderer(self, path, text):
		try:
			string = self.__get_string(path, 0)
			self.__validate(text)
			self.__model[path][0] = text
			self.__edit(path, 1)
#			self.__set_string(text)
		except ValueError:
			pass
		return False

	def __process_rplrenderer(self, path, text):
		self.__model[path][1] = text
#		self.__set_string(self.__model[path][0])
		return False

	def __set_string(self, string=None):
		try:
			if string: raise ValueError
			model, iterator = self.__treeview.get_selection().get_selected()
			self.__string = model.get_value(iterator, 0)
		except TypeError:
			self.__string = None
		except ValueError:
			self.__string = string
		return

	def __get_path(self):
		try:
			selection = self.__treeview.get_selection()
			model, iterator = selection.get_selected()
		except TypeError:
			raise ValueError
		return model.get_path(iterator)

	def __add(self):
		self.__sensitive(True)
		iterator = self.__model.append()
		path = self.__model.get_path(iterator)
		self.__edit(path, 0)
		return False

	def __edit(self, path=None, column=0):
		try:
			path = path if path else self.__get_path()
			column = self.__treeview.get_column(column)
			self.__treeview.set_cursor(path, column, start_editing=True)
		except ValueError:
			print "No selection found"
		return False

	def __get_last_iterator(self):
		if not len(self.__model): raise ValueError
		return self.__model[-1].iter

	def __delete(self):
		try:
			selection = self.__treeview.get_selection()
			model, iterator = selection.get_selected()
			key = model.get_value(iterator, 0)
			value = model.get_value(iterator, 1)
			is_valid = model.remove(iterator)
			self.__update = False
			self.__manager.emit("update-dictionary", (key, value, False))
			if is_valid is False: iterator =  self.__get_last_iterator()
			selection.select_iter(iterator)
			self.__treeview.grab_focus()
		except TypeError:
			from gettext import gettext as _
			print _("No selection found")
		except ValueError:
			sensitive = True if len(self.__model) else False
			self.__sensitive(sensitive)
		return False

	def __sensitive(self, sensitive=True):
		self.__treeview.set_property("sensitive", sensitive)
		self.__manager.emit("sensitive", sensitive)
		return False

	def __set_properties(self):
		self.__treeview.set_property("model", self.__model)
		self.__treeview.append_column(self.__abvcolumn)
		self.__treeview.append_column(self.__rplcolumn)
		return

	def __populate_model(self, dictionary):
		self.__treeview.handler_block(self.__sigid3)
		self.__sensitive(False)
		self.__treeview.set_model(None)
		self.__model.clear()
		for abbreviation, text in dictionary.items():
			self.__model.append([abbreviation, text])
		self.__treeview.set_model(self.__model)
		self.__editor.select_row(self.__treeview)
		sensitive = True if len(self.__model) else False
		self.__sensitive(sensitive)
		if sensitive: self.__treeview.grab_focus()
		self.__treeview.handler_unblock(self.__sigid3)
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __create_renderer(self):
		from gtk import CellRendererText
		renderer = CellRendererText()
		renderer.set_property("editable", True)
		return renderer

	def __create_abbreviation_column(self):
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from gettext import gettext as _
		column = TreeViewColumn(_("Abbreviation"), self.__abvrenderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_replacement_column(self):
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from gettext import gettext as _
		message = _("Expanded Text")
		column = TreeViewColumn(message, self.__rplrenderer, text=1)
		column.set_property("expand", True)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		return column

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __dictionary_cb(self, manager, dictionary):
		if self.__update: self.__populate_model(dictionary)
		self.__update = True
		return False

	def __changed_cb(self, *args):
		self.__set_string()
		return False

	def __abvedited_cb(self, renderer, path, text, *args):
		self.__process_abvrenderer(path, text)
		return False

	def __rpledited_cb(self, renderer, path, text, *args):
		self.__process_rplrenderer(path, text)
		return False

	def __row_changed_cb(self, model, path, iterator, *args):
		get_value = lambda column: model.get_value(iterator, column)
		self.__manager.emit("update-dictionary", (get_value(0), get_value(1), True))
		self.__update = False
		return False

	def __show_cb(self, *args):
		self.__unblock_row_changed_signal()
		self.__treeview.grab_focus()
		return False

	def __hide_cb(self, *args):
		self.__block_row_changed_signal()
		self.__treeview.grab_focus()
		return False

	def __event_cb(self, treeview, event):
		from gtk import keysyms
		if event.keyval != keysyms.Delete: return False
		self.__delete()
		return True

	def __edit_row_cb(self, *args):
		self.__edit()
		return False

	def __add_row_cb(self, *args):
		self.__add()
		return False

	def __delete_row_cb(self, *args):
		self.__delete()
		return False
