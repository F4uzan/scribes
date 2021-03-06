from SCRIBES.SignalConnectionManager import SignalManager

OFFSET = 4
REFRESH_TIME = 5 # units in milliseconds

class Animator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "slide", self.__slide_cb, True)
		self.connect(manager, "deltas", self.__deltas_cb)
		self.connect(manager, "bar-size", self.__bsize_cb)
		self.connect(manager, "view-size", self.__vsize_cb)
		self.connect(manager, "bar", self.__bar_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile, priority=PRIORITY_LOW)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__bar = None
		self.__start_point = 0
		self.__end_point = 0
		self.__hdelta = 0
		self.__vdelta = 0
		self.__bheight = 0
		self.__bwidth = 0
		self.__vheight = 0
		self.__vwidth = 0
		self.__busy = False
		self.__direction = ""
		self.__cycle_count = 0
		from SCRIBES.GObjectTimerManager import Manager
		self.__timer_manager = Manager()
		return

	def __slide(self, direction):
		self.__manager.emit("animation", "begin")
		self.__update_animation_start_point(direction)
		self.__update_animation_end_point(direction)
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(REFRESH_TIME, self.__move, direction, priority=PRIORITY_LOW)
		self.__timer_manager.add(self.__timer1)
		return False

	def __move(self, direction):
		try:
			self.__editor.refresh(False)
			if self.__cycle_count >= 50: raise AssertionError
			self.__cycle_count += 1
			animate = True
			self.__can_end(direction)
			from gobject import idle_add
			idle_add(self.__reposition_in, direction)
		except AssertionError:
			self.__timer_manager.remove_all()
			animate = False
			self.__editor.refresh(False)
			if direction == "down": self.__bar.hide()
			self.__editor.refresh(False)
			self.__manager.emit("animation", "end")
			self.__busy = False
			self.__cycle_count = 0
		return animate

	def __reposition_in(self, direction):
		try:
			x = int(self.__get_x(direction))
			y = int(self.__get_y(direction))
			self.__editor.refresh(False)
			self.__view.move_child(self.__bar, x, y)
			self.__editor.refresh(False)
			self.__bar.show_all()
			self.__editor.refresh(False)
		except AttributeError:
			pass
		return False

	def __can_end(self, direction):
		self.__editor.refresh(False)
		if direction == "down" and self.__start_point >= self.__end_point: raise AssertionError
		if direction == "up" and self.__start_point <= self.__end_point: raise AssertionError
		return False

	def __get_x(self, direction):
		self.__editor.refresh(False)
		if direction in ("up", "down"): return self.__vwidth - self.__bwidth + 4
		if direction == "left": self.__start_point -= self.__hdelta
		if direction == "right": self.__start_point += self.__hdelta
		x = self.__vwidth - self.__bwidth
		if self.__start_point <= x: return x + OFFSET
		return self.__start_point

	def __get_y(self, direction):
		self.__editor.refresh(False)
		if direction in ("left", "right"): return self.__vheight - self.__bheight + 4
		if direction == "up": self.__start_point -= self.__vdelta
		if direction == "down": self.__start_point += self.__vdelta
		return self.__start_point

	def __update_animation_start_point(self, direction):
		dictionary = {
			"up": self.__vheight,
			"down": self.__vheight - self.__bheight + 4,
			"left": self.__vwidth,
			"right":0,
		}
		self.__start_point = dictionary[direction]
		return False

	def __update_animation_end_point(self, direction):
		dictionary = {
			"up": self.__vheight - self.__bheight + 4,
			"down": self.__vheight + 4,
			"left": self.__vwidth - self.__bwidth + 4,
			"right": self.__bwidth,
		}
		self.__end_point = dictionary[direction]
		return False

	def __compile(self):
		self.__editor.optimize((self.__move, self.__reposition_in))
		return False

	def __destroy(self):
		self.__timer_manager.destroy()
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __slide_cb(self, manager, direction):
		if direction == self.__direction: return False
		self.__direction = direction
		if not self.__bar: return False
		self.__timer_manager.remove_all()
		self.__busy = True
		from gobject import idle_add, PRIORITY_LOW as LOW
		self.__timer2 = idle_add(self.__slide, direction, priority=LOW)
		self.__timer_manager.add(self.__timer2)
		return False

	def __deltas_cb(self, manager, deltas):
		self.__hdelta, self.__vdelta = deltas
		return False

	def __bsize_cb(self, manager, size):
		self.__bwidth, self.__bheight = size
		return False

	def __vsize_cb(self, manager, size):
		self.__vwidth, self.__vheight = size
		if self.__direction == "up": self.__reposition_in(self.__direction)
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		self.__bar.show_all()
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
