import struct

from engine.multiplayer.protocol.packet import Packet
from engine.multiplayer.protocol.packets.world.chunkDataPacket import ChunkDataPacket


class ChunkRequestPacket(Packet):
    def __init__(self, posList):
        super().__init__()
        self.posList = posList

    @staticmethod
    def encode(packet):
        buffer = struct.pack('i', len(packet.posList))
        for pos in packet.posList:
            buffer += struct.pack('ii', pos[0], pos[1])

        return buffer

    @staticmethod
    def decode(buffer):
        length = struct.unpack_from('i', buffer)[0]
        buffer = buffer[4:]
        posList = []

        for i in range(length):
            posList.append(struct.unpack_from("ii", buffer))
            buffer = buffer[8:]

        return ChunkRequestPacket(posList)

    def handle(self, context):
        world = context['terrain']
        networkHandler = context['networkHandler']
        networkConnector = context['networkConnector']

        chunks = [world.getChunkFromPos(pos[0], pos[1]) for pos in self.posList]
        packet = ChunkDataPacket(chunks)
        networkHandler.sendPacket(packet, networkConnector.player)
