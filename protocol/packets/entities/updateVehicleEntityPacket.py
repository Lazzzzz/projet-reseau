from engine.multiplayer.protocol.packet import Packet, UUIDToBytes, bytesToUUID


class UpdateVehicleEntityPacket(Packet):
	def __init__(self, entity, data=None):
		super().__init__()
		self.entity = entity
		self.data = data

	@staticmethod
	def encode(packet):
		buffer = UUIDToBytes(packet.entity.uuid)
		if packet.entity.vehicle:
			buffer += UUIDToBytes(packet.entity.vehicle.uuid)
		else:
			buffer += b'None'

		return buffer

	@staticmethod
	def decode(buffer):
		entityUUID, buffer = bytesToUUID(buffer)
		data = {
			'uuid': entityUUID,
			'vehicle': buffer
		}
		return UpdateVehicleEntityPacket(None, data=data)

	def handle(self, context):
		world = context['terrain']
		uuid = self.data['uuid']

		if uuid in world.entities:
			entity = world.entities[uuid]
			if self.data['vehicle'] == b'None':
				entity.setVehicles(None)
			else:
				vehicleUUID, _ = bytesToUUID(self.data['vehicle'])
				if vehicleUUID in world.entities:
					entity.setVehicles(world.entities[vehicleUUID])
