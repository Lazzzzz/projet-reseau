import time

from logic.simulation import SimulationSpace
from protocol.handler.serverNetworkHandler import ServerNetworkHandler
from protocol.packet import SERVER_SIDE
from protocol.packets.sendallpospacket import AllMousePosPacket
from protocol.packets.updatecirclepacket import UpdateCirclePacket
from protocol.packets.updaterectpacket import UpdateRectPacket
from register.initPacket import handlePacket, initPackets


class ServerHandler:
	def __init__(self, ip='localhost', port=5000):
		initPackets()
		
		self.connectionHandler = ServerNetworkHandler(ip, port)
		self.connectionHandler.start()
		
		self.timer = 0
		self.dt = 1 / 128
		
		self.simulation = SimulationSpace((640, 640))
		
		print("Server Open ip : {0} port : {1}".format(ip, port))
	
	def generateContext(self, connexion):
		return {
			'address': connexion.address,
			'networkHandler': self.connectionHandler,
			'networkConnector': connexion,
			'side': SERVER_SIDE,
			'simulation': self.simulation
		}
	
	def update(self):
		for connexion in self.connectionHandler.connexion:
			queuePacket = connexion.queuePacket.copy()
			for packet in queuePacket:
				handlePacket(packet['id'], packet['data'], self.generateContext(connexion))
			
			connexion.queuePacket.clear()
		
		self.simulation.update(self.dt)
		for rect_uuid in self.simulation.shapes['rect']:
			packet = UpdateRectPacket(self.simulation.shapes['rect'][rect_uuid])
			self.connectionHandler.sendPacketToAll(packet)
		
		for circle_uuid in self.simulation.shapes['circle']:
			packet = UpdateCirclePacket(self.simulation.shapes['circle'][circle_uuid])
			self.connectionHandler.sendPacketToAll(packet)
		
		packet = AllMousePosPacket(self.simulation.mouse)
		self.connectionHandler.sendPacketToAll(packet)
		
		time.sleep(self.dt)


server = ServerHandler()
while True:
	server.update()
