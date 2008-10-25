def main(argv):
	from operator import ne
	if ne(argv[0], "plugins"): raise RuntimeError
	files = __get_i18n_files(argv[0])
	__write_to_file(files)
	return

def __get_i18n_files(folder):
	from os import walk
	from operator import eq
	i18n_files = []
	for root, dirs, files in walk(folder):
		for filename in files:
			if filename.endswith("glade") or eq(filename, "i18n.py"):
				_file = root + "/" + filename + "\n"
				i18n_files.append(_file)
	return i18n_files

def __write_to_file(files):
	string = "".join(files)
	handle = open("i18n_plugin_files.txt", "w")
	handle.write(string)
	handle.close()
	return

if __name__ == "__main__":
	# Initialize the program.
	from sys import argv
	main(argv[1:])
