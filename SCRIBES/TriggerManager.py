# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that manages and activate triggers.
Triggers are operations mapped to keyboard shortcuts, widgets or
strings.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TriggerManager(object):
	"""
	This class manages and activates triggers. Triggers are operations
	mapped to accelerators, widgets or strings.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_2 = self.__editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_3 = self.__editor.connect("hide-bar", self.__hide_bar_cb)
		self.__signal_id_4 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_5 = self.__editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__editor.emit("initialized-trigger-manager")
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__window = editor.window
		self.__editor = editor
		# Precached list of accelerator keys
		self.__accelerator_keyname_list = set([])
		self.__bar_is_visible = False
		# Precached list of accelerator modifiers and keys
		self.__accelerators = set([])
		# A mapping of the format: {trigger_name: (trigger_object, accelerator)}
		self.__trigger_dictionary = {}
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__registration_id = editor.register_object()
		return

########################################################################
#
#							Public API
#
########################################################################

	def add_trigger(self, trigger):
		try:
			from Exceptions import InvalidTriggerNameError
			from Exceptions import DuplicateTriggerNameError
			from Exceptions import DuplicateTriggerRemovalError
			from Exceptions import DuplicateTriggerAcceleratorError
			accelerator = self.__format_accelerator(trigger.accelerator)
			self.__validate_trigger(trigger, accelerator)
			self.__trigger_dictionary[trigger.name] = trigger, accelerator
			self.__update_accelerator_info()
		except InvalidTriggerNameError:
			print "Error: %s is not a valid trigger name." % trigger.name
		except DuplicateTriggerNameError:
			print "Error: Another trigger named %s exists." % trigger.name
			print self.get_trigger_info(trigger.name)
		except DuplicateTriggerAcceleratorError:
			print "Error: Another trigger uses this accelerator %s." % trigger.accelerator
		except DuplicateTriggerRemovalError:
			print "Error: Duplicate trigger could not be forcefully removed"
			print "Error: %s will not be loaded" % trigger.name
		return

	def remove_trigger(self, trigger):
		try:
			name = trigger.name
			trigger.destroy()
			del trigger
			del self.__trigger_dictionary[name]
			self.__update_accelerator_info()
			if self.__trigger_dictionary: return
			if self.__is_quiting: self.__destroy()
		except KeyError:
			print "Error: Trigger named %s not found" % name
		return

	def add_triggers(self, triggers):
		return [self.add_trigger(trigger) for trigger in triggers]

	def remove_triggers(self, triggers):
		return [self.remove_trigger(trigger) for trigger in triggers]

	def trigger(self, trigger_name):
		self.__trigger_dictionary[trigger_name][0].activate()
		return

	def get_trigger_info(self, trigger):
		return

	def get_all_trigger_info(self):
		return self.__trigger_dictionary

	def get_trigger_names(self):
		return self.__trigger_dictionary.keys()

########################################################################

	def __validate_trigger(self, trigger, accelerator):
		from Exceptions import InvalidTriggerNameError
		from Exceptions import DuplicateTriggerNameError
		from Exceptions import DuplicateTriggerRemovalError
		from Exceptions import DuplicateTriggerAcceleratorError
		if not (trigger.name): raise InvalidTriggerNameError
		if trigger.name in self.__trigger_dictionary.keys():
			if trigger.error: raise DuplicateTriggerNameError
			trigger_object, accelerator = self.__trigger_dictionary[trigger.name]
			if not (trigger_object.removable): raise DuplicateTriggerRemovalError
			del self.__trigger_dictionary[trigger_object.name]
			trigger_object.destroy()
			return
		if not (accelerator): return
		for trigger_object, trigger_accelerator in self.__trigger_dictionary.values():
			if (accelerator == trigger_accelerator):
				if trigger.error:
					raise DuplicateTriggerAcceleratorError
				else:
					if not (trigger_object.removable): raise DuplicateTriggerRemovalError
					del self.__trigger_dictionary[trigger_object.name]
					trigger_object.destroy()
				break
		return

	def __format_accelerator(self, accelerator):
		if not (accelerator): return None
		accel_list = [accel.strip() for accel in accelerator.split("-")]
		accel = []
		for item in accel_list:
			if item in("Control", "control", "Ctrl", "ctrl"):
				accel.append("ctrl")
			elif item in ("Alt", "alt"):
				accel.append("alt")
			elif item in ("Shift", "shift"):
				accel.append("shift")
			else:
				accel.append(item)
		# Remove duplicate elements
		accel = set(accel)
		accel = list(accel)
		accel.sort()
		return tuple(accel)

	def __update_accelerator_info(self):
		modifiers = ("ctrl", "shift", "alt")
		keyname = set([])
		accelerators = set([])
		for trigger_object, accelerator in self.__trigger_dictionary.values():
			if not (accelerator): continue
			for item in accelerator:
				if item in modifiers: continue
				keyname.add(item)
			accelerators.add(accelerator)
		self.__accelerator_keyname_list = keyname
		self.__accelerators = accelerators
		return

	def __activate_accelerator(self, accelerator):
		accelerator.sort()
		accelerator = tuple(accelerator)
		if not (accelerator in self.__accelerators): return False
		for trigger, accel in self.__trigger_dictionary.values():
			if accel == accelerator:
				trigger.activate()
				break
		return True

	def __precompile_methods(self):
		methods = (self.__key_press_event_cb, self.__activate_accelerator,
				self.__update_accelerator_info, self.__format_accelerator)
		self.__editor.optimize(methods)
		return False

	def __destroy(self):
		self.__accelerator_keyname_list.clear()
		self.__trigger_dictionary.clear()
		self.__accelerators.clear()
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.window)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.unregister_object(self.__registration_id)
		del self
		self = None
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __key_press_event_cb(self, window, event):
		if self.__bar_is_visible: return False
		from gtk.gdk import CONTROL_MASK, MOD1_MASK, SHIFT_MASK, keyval_name
		keyname = keyval_name(event.keyval)
		if not(keyname in self.__accelerator_keyname_list): return False
		special_keys = ("Delete", "Insert", "Home", "End", "PageUp",
						"PageDown", "Right", "Left", "Up", "Down", "F1",
						"F12", "F10", "Return")
		# Control and Shift key are pressed.
		if event.state & CONTROL_MASK and event.state & SHIFT_MASK:
			if keyname in special_keys:
				accelerator = ["ctrl", "shift"] + [keyname]
			else:
				accelerator = ["ctrl"] + [keyname]
			return self.__activate_accelerator(accelerator)

		# Alt and Shift key are pressed.
		if event.state & SHIFT_MASK and event.state & MOD1_MASK:
			if keyname in special_keys:
				accelerator = ["alt", "shift"] + [keyname]
			else:
				accelerator = ["alt"] + [keyname]
			return self.__activate_accelerator(accelerator)

		# Control and Alt key are pressed.
		if event.state & CONTROL_MASK and event.state & MOD1_MASK:
			accelerator = ["alt", "ctrl"] + [keyname]
			return self.__activate_accelerator(accelerator)
		# Control key are pressed.
		if event.state & CONTROL_MASK:
			accelerator = ["ctrl"] + [keyname]
			return self.__activate_accelerator(accelerator)

		# Alt key is pressed.
		if event.state & MOD1_MASK:
			accelerator = ["alt"] + [keyname]
			return self.__activate_accelerator(accelerator)
		# No modifiers.
		return self.__activate_accelerator([keyname])

	def __close_document_cb(self, *args):
		self.__is_quiting = True
		return

	def __close_document_no_save_cb(self, *args):
		self.__is_quiting = True
		self.__destroy()
		return

	def __show_bar_cb(self, *args):
		self.__bar_is_visible = True
		return

	def __hide_bar_cb(self, *args):
		self.__bar_is_visible = False
		return
