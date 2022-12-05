import struct

from engine.helpers import constants
from engine.init.initTiles import getTileNameById
from engine.multiplayer.protocol.packet import Packet
from engine.terrain.chunk import WorldChunk


def encodeChunk(buffer, chunk):
    buffer += struct.pack('ii', chunk.rect.x, chunk.rect.y)
    for y in range(constants.CHUNK_SIZE):
        for x in range(constants.CHUNK_SIZE):
            buffer += struct.pack('i', chunk.tiles[y][x].id)

    return buffer


def decodeChunk(buffer):
    format = 'ii{0}i'.format(constants.CHUNK_SIZE * constants.CHUNK_SIZE)
    data = struct.unpack_from(format, buffer)
    x = data[0]
    y = data[1]
    chunk = WorldChunk(x, y)
    tilesData = data[2:]

    for y in range(constants.CHUNK_SIZE):
        for x in range(constants.CHUNK_SIZE):
            index = y * constants.CHUNK_SIZE + x
            chunk.setTile(x, y, getTileNameById(tilesData[index]))

    return chunk, buffer[struct.calcsize(format):]


class ChunkDataPacket(Packet):
    def __init__(self, chunksList):
        super().__init__()
        self.chunkList = chunksList

    @staticmethod
    def encode(packet):
        buffer = struct.pack("i", len(packet.chunkList))

        for chunk in packet.chunkList:
            buffer = encodeChunk(buffer, chunk)

        return buffer

    @staticmethod
    def decode(buffer):
        length = struct.unpack_from("ii", buffer)[0]
        buffer = buffer[4:]

        chunks = []
        for i in range(length):
            chunk, buffer = decodeChunk(buffer)
            chunks.append(chunk)

        return ChunkDataPacket(chunks)

    def handle(self, context):
        world = context['terrain']
        for chunk in self.chunkList:
            world.networkBuffer.removeChunkFromWait(chunk)
