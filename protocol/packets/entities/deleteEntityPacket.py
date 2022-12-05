from engine.multiplayer.protocol.packet import Packet, UUIDToBytes, bytesToUUID


class DeleteEntityPacket(Packet):
	def __init__(self, uuid):
		super().__init__()
		self.uuid = uuid

	@staticmethod
	def encode(packet):
		buffer = UUIDToBytes(packet.uuid)
		return buffer

	@staticmethod
	def decode(buffer):
		entityUUID, buffer = bytesToUUID(buffer)
		return DeleteEntityPacket(entityUUID)

	def handle(self, context):
		world = context['terrain']
		world.deleteEntity(self.uuid)
