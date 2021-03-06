from SCRIBES.SignalConnectionManager import SignalManager

HIDE_TIMER = 7000

class Timer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.__id = self.connect(editor.textview, "motion-notify-event", self.__motion_cb)
		self.connect(editor, "toolbar-is-visible", self.__visible_cb)
		self.connect(editor, "quit", self.__quit_cb)
		self.__block()
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__visible = False
		self.__blocked = None
		from SCRIBES.GObjectTimerManager import Manager
		self.__timer_manager = Manager()
		return

	def __destroy(self):
		self.__timer_manager.destroy()
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __hide(self):
		hide = lambda: self.__manager.emit("hide")
		from gobject import idle_add, PRIORITY_LOW
		self.__timer1 = idle_add(hide, priority=PRIORITY_LOW)
		self.__timer_manager.add(self.__timer1)
		return False

	def __block(self):
		if self.__blocked is True: return False
		self.__blocked = True
		self.__view.handler_block(self.__id)
		return False

	def __unblock(self):
		if self.__blocked is False: return False
		self.__blocked = False
		self.__view.handler_unblock(self.__id)
		return False

	def __motion_cb(self, *args):
		if self.__visible is False: return False
		self.__timer_manager.remove_all()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer2 = timeout_add(HIDE_TIMER, self.__hide, priority=PRIORITY_LOW)
		self.__timer_manager.add(self.__timer2)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __visible_cb(self, manager, visible):
		self.__visible = visible
		self.__unblock() if visible else self.__block()
		if visible is False: return False
		self.__timer_manager.remove_all()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer3 = timeout_add(HIDE_TIMER, self.__hide, priority=PRIORITY_LOW)
		self.__timer_manager.add(self.__timer3)
		return False
