# Permet de recevoir tous les data envoyer par les joueurs
import socket
from threading import Thread

from protocol.handler.networkConnector import NetworkConnector
from protocol.packet import SERVER_SIDE
from register.initPacket import sendPacket


class ServerNetworkHandler(Thread):
	def __init__(self, ip, port, max_connection=5):
		super().__init__()
		self.daemon = True
		self.ip = ip
		self.port = port
		self.connexion = []
		
		self.socket = socket.socket()
		self.socket.bind((self.ip, self.port))
		self.socket.listen(max_connection)
		
		self.close = False
	
	def sendPacket(self, packet, player):
		for connexion in self.connexion:
			if connexion.player == player:
				sendPacket(connexion.socket, packet, SERVER_SIDE)
				return
	
	def sendPacketToAll(self, packet):
		for connexion in self.connexion:
			if connexion.isConnected:
				sendPacket(connexion.socket, packet, SERVER_SIDE)
	
	def run(self) -> None:
		while not self.close:
			socket, address = self.socket.accept()
			handler = NetworkConnector(socket, address, self, SERVER_SIDE)
			self.connexion.append(handler)
			handler.start()
		
		self.socket.close()
