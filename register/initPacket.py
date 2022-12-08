from _socket import error

from protocol.packet import NetworkPacket, SERVER_SIDE, CLIENT_SIDE
from protocol.packets.createcirclepacket import CreateCirclePacket
from protocol.packets.createrectpacket import CreateRectPacket
from protocol.packets.sendallpospacket import AllMousePosPacket
from protocol.packets.sendmousepospacket import MousePosPacket
from protocol.packets.updatecirclepacket import UpdateCirclePacket
from protocol.packets.updaterectpacket import UpdateRectPacket

NETWORK_PACKETS_BY_ID = {}
NETWORK_PACKETS_BY_CLASS = {}
CONNECTION_ID = 0


def handlePacket(id, data, context):
	if data == b'':
		return
	
	NETWORK_PACKETS_BY_ID[id].decode(data, context)


def sendPacket(socket, packet, side):
	if packet.__class__ not in NETWORK_PACKETS_BY_CLASS:
		print("Packet {0} non initialiser".format(packet.__class__))
		exit(-1)
	
	networkPacket = NETWORK_PACKETS_BY_CLASS[packet.__class__]
	if networkPacket.side == side:
		try:
			data = networkPacket.encode(packet)
			socket.send(data)
			return True
		except error as exc:
			
			return False
	else:
		print('Packet send in the wrong way ...')
	
	return False


class PacketRegister:
	def __init__(self):
		self.packetId = 0
	
	def registerNetworkPacket(self, packetclass, side):
		if self.packetId in NETWORK_PACKETS_BY_ID:
			print('error network packet already register : {0}'.format(self.packetId))
			exit(-1)
		
		networkPacket = NetworkPacket(self.packetId, packetclass, side)
		NETWORK_PACKETS_BY_ID[self.packetId] = networkPacket
		NETWORK_PACKETS_BY_CLASS[packetclass] = networkPacket
		
		self.packetId += 1


def initPackets():
	register = PacketRegister()
	register.registerNetworkPacket(UpdateRectPacket, SERVER_SIDE)
	register.registerNetworkPacket(UpdateCirclePacket, SERVER_SIDE)
	register.registerNetworkPacket(CreateRectPacket, CLIENT_SIDE)
	register.registerNetworkPacket(CreateCirclePacket, CLIENT_SIDE)
	register.registerNetworkPacket(MousePosPacket, CLIENT_SIDE)
	register.registerNetworkPacket(AllMousePosPacket, SERVER_SIDE)
