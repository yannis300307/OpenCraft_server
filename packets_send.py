from packets_manager import WritePacket
from config import *


# tous les packets à envoyer

class LoginSuccessPacket:
    def __init__(self, client):
        self.packet = WritePacket(0)
        self.packet.write_int(client.id)
        self.packet.write_int((client.view_distance * 2) ** 3)

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class JoinWorldPacket:
    def __init__(self):
        self.packet = WritePacket(1)
        self.packet.write_float(DEFAULT_SPAWN_POS[0])
        self.packet.write_float(DEFAULT_SPAWN_POS[1])
        self.packet.write_float(DEFAULT_SPAWN_POS[2])
        self.packet.write_float(DEFAULT_DIR[0])
        self.packet.write_float(DEFAULT_DIR[1])

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class KickPacket:
    def __init__(self, reason):
        self.packet = WritePacket(2)
        self.packet.write_string(reason)

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class ChatPacket:
    def __init__(self, message):
        self.packet = WritePacket(3)
        self.packet.write_string(message)

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class ChunkUpdatePacket:
    def __init__(self, chunk):
        self.packet = WritePacket(4)
        self.packet.write_int(chunk.pos[0])
        self.packet.write_int(chunk.pos[1])
        self.packet.write_int(chunk.pos[2])
        blocks = []
        for block in chunk.blocks:
            blocks.append(BLOCKS[block.type])
        self.packet.write_bytes(blocks)

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class BlockUpdatePacket:
    def __init__(self, block):
        self.packet = WritePacket(5)
        self.packet.write_int(block.globalpos[0])
        self.packet.write_int(block.globalpos[1])
        self.packet.write_int(block.globalpos[2])
        self.packet.write_byte(BLOCKS[block.type])

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class SpawnEntityPacket:
    def __init__(self, entity):
        self.packet = WritePacket(6)
        self.packet.write_int(entity.id)
        self.packet.write_byte(ENTITIES[entity.type])
        self.packet.write_float(entity.pos[0])
        self.packet.write_float(entity.pos[1])
        self.packet.write_float(entity.pos[2])
        self.packet.write_float(entity.dir[0])
        self.packet.write_float(entity.dir[1])

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class RemoveEntityPacket:
    def __init__(self, entity):
        self.packet = WritePacket(7)
        self.packet.write_int(entity.id)

    def send_to(self, client):
        client.send(self.packet.get_bytes())

class EntityMovementPacket:
    def __init__(self, entity, imperative):
        self.packet = WritePacket(8)
        self.packet.write_int(entity.id)
        self.packet.write_float(entity.pos[0])
        self.packet.write_float(entity.pos[1])
        self.packet.write_float(entity.pos[2])
        self.packet.write_float(entity.dir[0])
        self.packet.write_float(entity.dir[1])
        self.imperative = imperative

    def send_to(self, client):
        client.send(self.packet.get_bytes(), self.imperative)
