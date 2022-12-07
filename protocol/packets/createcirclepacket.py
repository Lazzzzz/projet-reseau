from logic.simulation import Circle
from protocol.packet import intToBytes, bytesToInt, Packet, floatToBytes, bytesToFloat, UUIDToBytes, bytesToUUID


class CreateCirclePacket(Packet):
	def __init__(self, circle: Circle):
		super().__init__()
		self.circle = circle
	
	@staticmethod
	def encode(packet):
		x = packet.circle.body.position[0]
		y = packet.circle.body.position[1]
		
		buffer = floatToBytes(x)
		buffer += floatToBytes(y)
		
		buffer += floatToBytes(packet.circle.body.mass)
		
		buffer += intToBytes(packet.circle.radius)
		
		buffer += UUIDToBytes(packet.circle.uuid)
		
		return buffer
	
	@staticmethod
	def decode(buffer):
		x, buffer = bytesToFloat(buffer)
		y, buffer = bytesToFloat(buffer)
		
		m, buffer = bytesToFloat(buffer)
		
		r, buffer = bytesToInt(buffer)
		
		uuid, _ = bytesToUUID(buffer)
		
		circle = Circle(x, y, r, m)
		circle.uuid = uuid
		
		return CreateCirclePacket(circle)
	
	def handle(self, context):
		simulation = context['simulation']
		simulation.add_shape(self.circle)
