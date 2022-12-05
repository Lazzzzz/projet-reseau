import time

from protocol.handler.serverNetworkHandler import ServerNetworkHandler
from protocol.packet import SERVER_SIDE
from register.initPacket import handlePacket, initPackets


class ServerHandler:
	def __init__(self, ip='localhost', port=5000):
		initPackets()
		
		self.connectionHandler = ServerNetworkHandler(ip, port)
		self.connectionHandler.start()
		
		self.timer = 0
		self.dt = 1 / 64
		
		print("Server Open ip : {0} port : {1}".format(ip, port))
	
	def generateContext(self, connexion):
		return {
			'address': connexion.address,
			'networkHandler': self.connectionHandler,
			'networkConnector': connexion,
			'side': SERVER_SIDE
		}
	
	def update(self):
		for connexion in self.connectionHandler.connexion:
			queuePacket = connexion.queuePacket.copy()
			for packet in queuePacket:
				handlePacket(packet['id'], packet['data'], self.generateContext(connexion))
			
			connexion.queuePacket.clear()
		
		time.sleep(self.dt)
