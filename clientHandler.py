import time

from engine.entities.player.playerEntity import Player
from engine.entities.vehicules.base import Vehicle
from engine.init.initPacket import NETWORK_PACKETS_BY_ID
from engine.multiplayer.protocol.handler.clientNetworkHandler import ClientNetworkHandler
from engine.multiplayer.protocol.packets.entities.player.playerPacket import PlayerPacket
from engine.terrain.world.clientWorld import ClientWorld


class ClientHandler:
	def __init__(self):
		self.networkConnector = None
		self.world = ClientWorld()
		self.player = Player()

		self.world.spawnEntity(self.player)

		self.connect()

		self.time = time.time()
		self.total_time = 0

	def connect(self, ip='localhost', port=5001):
		if len(NETWORK_PACKETS_BY_ID) == 0:
			print('Packet non init')
			exit(-1)

		self.networkConnector = ClientNetworkHandler(ip, port, self.player.uuid, self.world)
		self.world.setConnection(self.networkConnector)
		self.networkConnector.connector.player = self.player

	def isConnected(self):
		if self.networkConnector is None:
			return False

		return self.networkConnector.isConnected()

	def update(self):
		tick = self.world.properties.tick

		dtime = time.time() - self.time
		self.total_time += dtime
		self.time = time.time()

		if self.networkConnector is None:
			return

		if self.total_time > 1 / tick:
			self.networkConnector.update()
			self.world.update(self.player)
			self.total_time -= 1 / tick

		playerPacket = PlayerPacket(self.player)
		self.networkConnector.sendPacket(playerPacket)

		# print(time.time() - self.time)

		if self.player.vehicle is None:
			for e in self.world.entities:
				e = self.world.entities[e]
				if isinstance(e, Vehicle):
					self.player.setVehicles(e)
					pass
