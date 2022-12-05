from clientHandler import ClientHandler
from serverHandler import ServerHandler


def print_hi():
	server = ServerHandler()
	client = ClientHandler()
	
	while True:
		server.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	print_hi()
