from protocol.packet import NetworkPacket, CLIENT_SIDE
from protocol.packets.connectionPacket import ConnectionPacket

NETWORK_PACKETS_BY_ID = {}
NETWORK_PACKETS_BY_CLASS = {}
CONNECTION_ID = 0


def handlePacket(id, data, context):
	if data == b'':
		return
	
	NETWORK_PACKETS_BY_ID[id].decode(data, context)


def sendPacket(socket, tick, packet, side):
	if packet.__class__ not in NETWORK_PACKETS_BY_CLASS:
		print("Packet {0} non initialiser".format(packet.__class__))
		exit(-1)
	
	networkPacket = NETWORK_PACKETS_BY_CLASS[packet.__class__]
	if networkPacket.side == side:
		data = networkPacket.encode(tick, packet)
		socket.send(data)
	else:
		print('Packet send in the wrong way ...')


class PacketRegister:
	def __init__(self):
		self.packetId = 0
	
	def registerNetworkPacket(self, packetclass, side):
		if self.packetId in NETWORK_PACKETS_BY_ID:
			print('error network packet already register : {0}'.format(id))
			exit(-1)
		
		networkPacket = NetworkPacket(self.packetId, packetclass, side)
		NETWORK_PACKETS_BY_ID[self.packetId] = networkPacket
		NETWORK_PACKETS_BY_CLASS[packetclass] = networkPacket
		
		self.packetId += 1


def initPackets():
	register = PacketRegister()
	register.registerNetworkPacket(ConnectionPacket, CLIENT_SIDE)
