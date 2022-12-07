from protocol.packet import Packet, intToBytes, bytesToInt, UUIDToBytes, bytesToUUID


class AllMousePosPacket(Packet):
	def __init__(self, pos):
		super().__init__()
		self.pos = pos
	
	@staticmethod
	def encode(packet):
		size = len(packet.pos)
		
		buffer = intToBytes(size)
		
		for uuid in packet.pos:
			x = packet.pos[uuid][0]
			y = packet.pos[uuid][1]
			buffer += intToBytes(x)
			buffer += intToBytes(y)
			buffer += UUIDToBytes(uuid)
		
		return buffer
	
	@staticmethod
	def decode(buffer):
		result = {}
		
		size, buffer = bytesToInt(buffer)
		for i in range(size):
			x, buffer = bytesToInt(buffer)
			y, buffer = bytesToInt(buffer)
			uuid, buffer = bytesToUUID(buffer)
			result[uuid] = (x, y)
		
		return AllMousePosPacket(result)
	
	def handle(self, context):
		app = context['app']
		app.mouse_pos = self.pos
