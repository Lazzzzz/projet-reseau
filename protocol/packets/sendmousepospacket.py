from protocol.packet import Packet, intToBytes, bytesToInt


class MousePosPacket(Packet):
	def __init__(self, pos):
		super().__init__()
		self.pos = pos
	
	@staticmethod
	def encode(packet):
		x = packet.pos[0]
		y = packet.pos[1]
		
		buffer = intToBytes(x)
		buffer += intToBytes(y)
		
		return buffer
	
	@staticmethod
	def decode(buffer):
		x, buffer = bytesToInt(buffer)
		y, buffer = bytesToInt(buffer)
		
		return MousePosPacket((x, y))
	
	def handle(self, context):
		simulation = context['simulation']
		print(self.pos)
