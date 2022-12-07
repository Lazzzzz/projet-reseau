import socket

from protocol.handler.networkConnector import NetworkConnector
from protocol.packet import CLIENT_SIDE
from register.initPacket import sendPacket, handlePacket


class ClientNetworkHandler():
	def __init__(self, ip, port, uuid, app):
		super().__init__()
		self.app = app
		
		self.serverIp = ip
		self.serverPort = port
		
		self.address = (self.serverIp, self.serverPort)
		self.uuid = uuid
		
		self.socket = socket.socket()
		self.socket.connect(self.address)
		self.socket.settimeout(15)
		
		self.close = False
		
		self.connector = NetworkConnector(self.socket, self.address, self, CLIENT_SIDE)
		self.connector.start()
	
	def sendPacket(self, packet):
		sendPacket(self.socket, packet, CLIENT_SIDE)
	
	def generateContext(self):
		return {
			'address': self.address,
			'networkHandler': self,
			'networkConnector': self.connector,
			'side': CLIENT_SIDE,
			'app': self.app
		}
	
	def update(self):
		queuePacket = self.connector.queuePacket.copy()
		for packet in queuePacket:
			handlePacket(packet['id'], packet['data'], self.generateContext())
		
		self.connector.queuePacket.clear()
	
	def isConnected(self):
		return self.connector.isConnected
