from protocol.packet import Packet, intToBytes, bytesToInt, UUIDToBytes, bytesToUUID


class MousePosPacket(Packet):
	def __init__(self, pos, uuid):
		super().__init__()
		self.pos = pos
		self.uuid = uuid
	
	@staticmethod
	def encode(packet):
		x = packet.pos[0]
		y = packet.pos[1]
		
		buffer = intToBytes(x)
		buffer += intToBytes(y)
		buffer += UUIDToBytes(packet.uuid)
		
		return buffer
	
	@staticmethod
	def decode(buffer):
		x, buffer = bytesToInt(buffer)
		y, buffer = bytesToInt(buffer)
		
		uuid, _ = bytesToUUID(buffer)
		
		return MousePosPacket((x, y), uuid)
	
	def handle(self, context):
		simulation = context['simulation']
		simulation.mouse[self.uuid] = self.pos
