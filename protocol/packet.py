import struct
import uuid
from uuid import UUID

CLIENT_SIDE = 'client_side'
SERVER_SIDE = 'server_side'
BOTH = 'both'


class Packet:
	def __init__(self):
		pass
	
	@staticmethod
	def encode(packet):
		pass
	
	@staticmethod
	def decode(buffer):
		return None
	
	def handle(self, context):
		pass


class NetworkPacket:
	def __init__(self, id, packetclass, side):
		self.id = id
		self.packetclass = packetclass
		self.side = side
	
	def encode(self, packet):
		packet_id = struct.pack("i", self.id)
		buffer = self.packetclass.encode(packet)
		
		size = struct.pack("i", len(buffer))
		
		return size + packet_id + buffer
	
	def decode(self, buffer: bytes, context):
		packet = self.packetclass.decode(buffer)
		packet.handle(context)


def UUIDToBytes(uuid: UUID):
	return struct.pack('<QBBHHL', *uuid.fields[::-1])


def bytesToUUID(buffer):
	return uuid.UUID(fields=struct.unpack_from('<QBBHHL', buffer)[::-1]), buffer[struct.calcsize('<QBBHHL'):]


def intToBytes(i):
	return struct.pack('i', i)


def bytesToInt(buffer):
	return struct.unpack_from('i', buffer)[0], buffer[struct.calcsize('i'):]


def floatToBytes(f):
	return struct.pack('f', f)


def bytesToFloat(buffer):
	return struct.unpack_from('f', buffer)[0], buffer[struct.calcsize('f'):]


def doubleToBytes(d):
	return struct.pack('d', d)


def bytesToDouble(buffer):
	return struct.unpack_from('d', buffer)[0], buffer[struct.calcsize('d'):]


def boolToBytes(b):
	return struct.pack('?', b)


def bytesToBool(buffer):
	return struct.unpack_from('?', buffer)[0], buffer[struct.calcsize('?'):]
