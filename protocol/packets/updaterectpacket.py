from logic.simulation import Rect
from protocol.packet import intToBytes, bytesToInt, Packet, floatToBytes, bytesToFloat, UUIDToBytes, bytesToUUID


class UpdateRectPacket(Packet):
	def __init__(self, rect: Rect):
		super().__init__()
		self.rect = rect
	
	@staticmethod
	def encode(packet):
		x = packet.rect.body.position[0]
		y = packet.rect.body.position[1]
		
		buffer = floatToBytes(x)
		buffer += floatToBytes(y)
		
		buffer += floatToBytes(packet.rect.body.mass)
		
		buffer += intToBytes(packet.rect.rect.w)
		buffer += intToBytes(packet.rect.rect.h)
		
		buffer += UUIDToBytes(packet.rect.uuid)
		
		return buffer
	
	@staticmethod
	def decode(buffer):
		x, buffer = bytesToFloat(buffer)
		y, buffer = bytesToFloat(buffer)
		
		m, buffer = bytesToFloat(buffer)
		
		w, buffer = bytesToInt(buffer)
		h, buffer = bytesToInt(buffer)
		
		uuid, _ = bytesToUUID(buffer)
		
		rect = Rect(x, y, w, h, m)
		rect.uuid = uuid
		
		return UpdateRectPacket(rect)
	
	def handle(self, context):
		app = context['app']
		app.objects['rect'][self.rect.uuid] = self.rect
