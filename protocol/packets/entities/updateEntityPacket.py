from engine.init.initEntities import ENTITIES_BY_CLASS, ENTITIES_BY_ID
from engine.multiplayer.protocol.packet import Packet, intToBytes, UUIDToBytes, bytesToInt, bytesToUUID


class UpdateEntityPacket(Packet):
	def __init__(self, entity, data=None):
		super().__init__()
		self.entity = entity
		self.data = data

	@staticmethod
	def encode(packet):
		entityID = ENTITIES_BY_CLASS[packet.entity.__class__].id

		buffer = intToBytes(entityID)
		buffer += UUIDToBytes(packet.entity.uuid)
		buffer += packet.entity.save()

		return buffer

	@staticmethod
	def decode(buffer):
		entityID, buffer = bytesToInt(buffer)
		entityUUID, buffer = bytesToUUID(buffer)
		data = {
			'id': entityID,
			'uuid': entityUUID,
			'save': buffer
		}

		return UpdateEntityPacket(None, data=data)

	def handle(self, context):
		world = context['terrain']
		entityId = self.data['id']
		uuid_entity = self.data['uuid']
		networkConnector = context['networkConnector']

		if networkConnector.player is None:
			return

		if uuid_entity == networkConnector.player.uuid:
			return
		# uuid_entity = uuid.UUID(int=0)

		if uuid_entity in world.entities:
			world.entities[uuid_entity].load(self.data['save'])
		else:
			entity = ENTITIES_BY_ID[entityId].entity()
			entity.uuid = uuid_entity
			world.spawnEntity(entity)
			entity.load(self.data['save'])
