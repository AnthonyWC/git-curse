def log(filename, message):
	with open(filename, 'a') as f:
		f.write(message)
		f.write("\n")