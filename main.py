from serverHandler import ServerHandler


def print_hi():
	server = ServerHandler(ip='10.10.59.162')
	
	while True:
		server.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	print_hi()
