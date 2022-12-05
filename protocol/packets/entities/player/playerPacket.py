from engine.multiplayer.protocol.packet import Packet


class PlayerPacket(Packet):
	def __init__(self, player, data=None):
		super().__init__()
		self.player = player
		self.data = data

	@staticmethod
	def encode(packet):
		buffer = packet.player.save()
		return buffer

	@staticmethod
	def decode(buffer):
		return PlayerPacket(None, data=buffer)

	def handle(self, context):
		network = context['networkConnector']
		if network.player is not None:
			network.player.load(self.data)
			network.player.loadBuffer(network.player.buffer[0])
			network.player.buffer = network.player.buffer[1:]
