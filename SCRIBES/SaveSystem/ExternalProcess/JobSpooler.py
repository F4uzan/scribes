class Spooler(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("save-data", self.__new_job_cb)
		manager.connect_after("saved-data", self.__finished_cb)
		manager.connect_after("error", self.__finished_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		from collections import deque
		self.__jobs = deque()
		self.__busy = False
		return

	def __check(self):
		if self.__busy or not self.__jobs: return False
		self.__send(self.__jobs.pop())
		return False

	def __send(self, data):
		self.__busy = True
		self.__manager.emit("encode-text", data)
		return False

	def __new_job(self, data):
		self.__jobs.appendleft(data)
		self.__check()
		return False

	def __new_job_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__new_job, data)
		return False

	def __finished_cb(self, *args):
		self.__busy = False
		self.__check()
		return False