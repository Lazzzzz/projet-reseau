from protocol.packet import Packet, UUIDToBytes, bytesToUUID


class ConnectionPacket(Packet):
	def __init__(self, uuid):
		super().__init__()
		self.uuid = uuid
	
	@staticmethod
	def encode(packet):
		buffer = UUIDToBytes(packet.uuid)
		return buffer
	
	@staticmethod
	def decode(buffer):
		uuid, _ = bytesToUUID(buffer)
		return ConnectionPacket(uuid)
	
	def handle(self, context):
		address = context['address']
		
		connection = {
			'player_uuid': self.uuid,
			'address': address
		}
		print('\n{0} : Connected\n'.format(connection))
