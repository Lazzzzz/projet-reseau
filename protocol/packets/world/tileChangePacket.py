import struct

from engine.init.initTiles import getTileNameById
from engine.multiplayer.protocol.packet import Packet
from engine.terrain.world.worldUtils import World


class TileChangePacket(Packet):
    def __init__(self, x, y, tile_id):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_id = tile_id

    @staticmethod
    def encode(packet):
        buffer = struct.pack('iii', packet.x, packet.y, packet.tile_id)
        return buffer

    @staticmethod
    def decode(buffer):
        data = struct.unpack('iii', buffer)
        x = data[0]
        y = data[1]
        tile_id = data[2]
        return TileChangePacket(x, y, tile_id)

    def handle(self, context):
        world: World = context['terrain']
        world.setTile(self.x, self.y, getTileNameById(self.tile_id))
