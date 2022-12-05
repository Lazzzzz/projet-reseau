from engine.multiplayer.protocol.packet import Packet
from engine.terrain.world.worldProperties import WorldProperties


class ServerInfoPacket(Packet):
	def __init__(self, worldProperties):
		super().__init__()
		self.worldProperties = worldProperties

	@staticmethod
	def encode(packet):
		buffer = packet.worldProperties.save()
		return buffer

	@staticmethod
	def decode(buffer):
		worldProperties = WorldProperties()
		worldProperties.load(buffer)
		return ServerInfoPacket(worldProperties)

	def handle(self, context):
		networkConnector = context['networkConnector']
		address = context['address']
		world = context['terrain']

		print(self.worldProperties)
