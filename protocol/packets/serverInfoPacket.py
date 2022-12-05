from protocol.packet import intToBytes, bytesToInt, Packet


class ServerInfoPacket(Packet):
	def __init__(self, numero1, numero2):
		super().__init__()
		self.numero1 = numero1
		self.n2 = numero2
	
	@staticmethod
	def encode(packet):
		buffer = intToBytes(packet.numero1)
		buffer += intToBytes(packet.n2)
		return buffer
	
	@staticmethod
	def decode(buffer):
		n1, buffer = bytesToInt(buffer)
		n2, _ = bytesToInt(buffer)
		return ServerInfoPacket(n1, n2)
	
	def handle(self, context):
		print(self.numero1, self.n2)
