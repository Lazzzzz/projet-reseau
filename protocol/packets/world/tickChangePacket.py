from engine.multiplayer.protocol.packet import Packet, intToBytes, bytesToInt


class TickChangePacket(Packet):
	def __init__(self, tick):
		super().__init__()
		self.tick = tick

	@staticmethod
	def encode(packet):
		buffer = intToBytes(packet.tick)
		return buffer

	@staticmethod
	def decode(buffer):
		tick, _ = bytesToInt(buffer)
		return TickChangePacket(tick)

	def handle(self, context):
		pass
