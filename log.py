import datetime
def log(filename, message):
	with open(filename, 'a') as f:
		f.write(datetime.datetime.time(datetime.datetime.now()).strftime("%I:%M:%S %p "))
		f.write(message)
		f.write("\n")