import time
import uuid

from protocol.handler.clientNetworkHandler import ClientNetworkHandler


class ClientHandler:
	def __init__(self, ip='localhost', port=5000):
		self.networkConnector = ClientNetworkHandler(ip, port, uuid.uuid4())
		
		self.time = time.time()
		self.total_time = 0
	
	def update(self):
		pass
