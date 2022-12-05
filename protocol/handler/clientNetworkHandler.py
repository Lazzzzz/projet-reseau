import socket
from threading import Thread

from server.protocol.handler.networkConnector import NetworkConnector
from server.protocol.packet import CLIENT_SIDE
from server.protocol.packets.connectionPacket import ConnectionPacket


class ClientNetworkHandler(Thread):
	def __init__(self, ip, port, uuid):
		super().__init__()
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
		
		packet = ConnectionPacket(self.uuid)
		self.sendPacket(packet)
	
	def sendPacket(self, packet):
		sendPacket(self.socket, packet, CLIENT_SIDE)
	
	def generateContext(self):
		return {
			'terrain': self.world,
			'address': self.address,
			'networkHandler': self,
			'networkConnector': self.connector,
			'side': CLIENT_SIDE
		}
	
	def update(self):
		queuePacket = self.connector.queuePacket.copy()
		for packet in queuePacket:
			handlePacket(packet['id'], packet['data'], self.generateContext())
		
		self.connector.queuePacket.clear()
	
	def isConnected(self):
		return self.connector.isConnected
