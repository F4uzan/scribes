from Utils import open_database
basepath = "/Preferences/Languages/Font.gdb"

def get_value(language):
	try:
		font = "Monospace 12"
		database = open_database(basepath, "r")
		font = database[language]
	except KeyError:
		pass
	finally:
		database.close()
	return font

def set_value(data):
	try:
		language, font = data
		database = open_database(basepath, "w")
		database[language] = font
	finally:
		database.close()
	return

def reset(language):
	try:
		database = open_database(basepath, "w")
		del database[language]
	except KeyError:
		pass
	finally:
		database.close()
	return
