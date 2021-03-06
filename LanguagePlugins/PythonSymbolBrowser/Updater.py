class Updater(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("show-window", self.__show_window_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from collections import deque
		# symbols has the format [(line_number, name, type), ...]
		self.__symbols = deque([])
		self.__depth = 0
		self.__inside_class = False
		self.__class_depth = 0
		self.__function_depth = 0
		return

	def __get_symbols(self):
		try:
			self.__symbols.clear()
			from compiler import parse
			parse_tree = parse(self.__editor.text)
			nodes = parse_tree.getChildNodes()
			self.__extract_symbols(nodes, 0)
			self.__manager.emit("update", self.__symbols)
		except SyntaxError:
			pass
		return False

	def __extract_symbols(self, nodes, depth):
		self.__depth = depth
		class_flag = False
		function_flag = False
		for node in nodes:
			if self.__is_function_node(node):
				function_flag = True
				if self.__function_depth:
					value = "Function"
				else:
					value = "Method" if self.__class_depth else "Function"
				pixbuf = self.__manager.function_pixbuf if value == "Function" else self.__manager.method_pixbuf
				self.__symbols.append((node.lineno, node.name, value, depth, pixbuf))
				self.__function_depth += 1
			if self.__is_class_node(node):
				class_flag = True
				self.__symbols.append((node.lineno, node.name, "Class", depth, self.__manager.class_pixbuf))
				self.__class_depth	+= 1
			self.__extract_symbols(node.getChildNodes(), depth+1)
			if class_flag: self.__class_depth -= 1
			if function_flag: self.__function_depth -= 1
			class_flag = False
			function_flag = False
		return

	def __is_function_node(self, node):
		attributes = set(["decorators", "name", "argnames", "defaults", "flags", "doc", "code"])
		return attributes.issubset(set(dir(node)))

	def __is_class_node(self, node):
		attributes = set(["name", "bases", "doc", "code"])
		return attributes.issubset(set(dir(node)))

	def __precompile_methods(self):
		methods = (self.__extract_symbols, self.__get_symbols,)
		self.__editor.optimize(methods)
		return False

	def __show_window_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__get_symbols, priority=9999)
		return
