import struct
from threading import Thread

from protocol.packet import SERVER_SIDE

MAX_RECV_SIZE = 2048


class NetworkConnector(Thread):
	def __init__(self, socket, address, networkHandler, side):
		super().__init__()
		self.daemon = True
		self.socket = socket
		self.address = address
		self.isConnected = True
		self.side = side
		
		self.buffer = b''
		
		self.player = None
		
		self.networkHandler = networkHandler
		
		self.socket.settimeout(15)
		
		self.queuePacket = []
		self.shouldUpdate = False
		self.tick = 0
	
	def handleData(self, data):
		buffer = self.buffer + data
		try:
			while True:
				if len(buffer) < 8:
					self.buffer = buffer
					break
				
				packetLength = struct.unpack_from('i', buffer)[0]
				packetId = struct.unpack_from('i', buffer, 4)[0]
				
				# 8 bits for the 2 int (lenght, id, tick)
				if len(buffer) >= 8 + packetLength:
					dataPacket = buffer[8:8 + packetLength]
					buffer = buffer[8 + packetLength:]
					packet = {'id': packetId, 'data': dataPacket}
					
					self.queuePacket.append(packet)
				else:
					self.buffer = buffer
					break
		
		except Exception as e:
			self.buffer = b''
			print(e)
	
	def run(self) -> None:
		while self.isConnected:
			try:
				data = self.socket.recv(MAX_RECV_SIZE)
				self.handleData(data)
			except Exception as e:
				self.isConnected = False
				
				if self.side == SERVER_SIDE:
					self.networkHandler.connexion.remove(self)
					print('Deconnected : {0} | Reason {1}'.format(self.player.uuid, e))
		
		self.socket.close()
