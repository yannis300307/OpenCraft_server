from config import *
from chunk import Chunk
from utils import *
from packets_send import ChunkUpdatePacket, SpawnEntityPacket, BlockUpdatePacket
from block import Block

class World:
    """Représente le monde"""
    def __init__(self, tcp_clients, noise, logs):
        self.noise = noise
        self.tcp_clients = tcp_clients
        self.chunks = {}
        self.entities = {}
        self.logs = logs
        self.chunks_index = {}
        self.last_id = 0
        self.charge_from_file()

    def get_chunk_in_pos(self, pos: (), addx=0, addy=0, addz=0):  # retourne le chunk à la position donnée
        ret = self.chunks.get(
            (to_chunk(pos[0])+addx, to_chunk(pos[1])+addy, to_chunk(pos[2])+addz))
        if ret is None:
            world_file = open(DEFAULT_WORLD_FILE, "br")
            size = int.from_bytes(world_file.read(4), "big")
            chunks = world_file.read()[size*16:]
            pos_ = (to_chunk(pos[0])+addx, to_chunk(pos[1])+addy, to_chunk(pos[2])+addz)
            if pos_ in list(self.chunks_index.keys()):
                chunk = chunks[self.chunks_index[pos_]*BLOCKS_FOR_CHUNK: self.chunks_index[pos_]*BLOCKS_FOR_CHUNK+BLOCKS_FOR_CHUNK]
                chunk_ = Chunk(pos_, self.noise)
                for block_ in range(len(chunk)):
                    chunk_.blocks[block_].type = BLOCKS_ID[chunk[block_]]
        return ret

    def load_chunks_surroundings(self, pos: (), distance: int, client, charged_chunks):  # charge les chunks alentours et les envoient au client donné
        chunk_charged = 0
        chunks = []
        for y in range(-distance, min(distance, ceil_of_multiple(pos[1], 16))):
            for x in range(-distance, distance):
                for z in range(-distance, distance):
                    if client.connected:
                        tpos = (to_chunk(pos[0])+x, to_chunk(pos[1])+y, to_chunk(pos[2])+z)
                        chunk = self.get_chunk_in_pos(pos, x, y, z)
                        if not tpos in charged_chunks:
                            self.logs.write(
                                "Chargement du chuk à la position x=" + str(x) + " y=" + str(y) + " z=" + str(z),
                                print_=False)
                            chunk_charged += 1
                            if chunk is None:
                                self.chunks[tpos] = Chunk(tpos, self.noise)
                                chunk = self.chunks[tpos]
                                self.chunks[tpos].gen_chunk()
                            packet = ChunkUpdatePacket(chunk)
                            packet.send_to(client)
                            del packet
                        chunks.append(tpos)
                    else:
                        return
        return chunks

    def set_block(self, pos, type_, clientt):
        chunk = self.get_chunk_in_pos(pos, 0, 0, 0)
        if chunk is not None:
            block = chunk.get_block((to_local(pos[0]), to_local(pos[1]), to_local(pos[2])))
            block.type = type_
            packet = BlockUpdatePacket(block)
            for client in self.tcp_clients:
                if client != clientt:
                    packet.send_to(client)

    def spawn_entities(self, client):  # fait spawner toutes les entités au client donné
        for id_ in self.entities:
            entity = self.entities[id_]
            packet = SpawnEntityPacket(entity)
            if entity.is_spawned and entity != client:
                packet.send_to(client)

    def update_entities(self, id_, x, y, z, pitch, yaw):  # update la position des entitées
        entity = self.entities[id_]
        entity.dir = [pitch, yaw]
        entity.set_pos((x, y, z), entity.dir)

    def save(self):
        self.logs.write("Enregistrement du monde...")
        data = b""
        data += len(list(self.chunks.values())).to_bytes(4, "big", signed=False)
        pos_list = list(self.chunks.keys())
        index = 0
        self.logs.write("Ajout des indexs...")
        for chunk in pos_list:
            data += chunk[0].to_bytes(4, "big", signed=True)
            data += chunk[1].to_bytes(4, "big", signed=True)
            data += chunk[2].to_bytes(4, "big", signed=True)
            data += index.to_bytes(4, "big")
        self.logs.write("Ajout des chunks...")
        for chunk in pos_list:
            data += self.chunks[chunk].get_bytes_array()
        self.logs.write("Enregistrement dans le fichier de sauvegarde du monde ...")
        world_file = open(DEFAULT_WORLD_FILE, "bw")
        world_file.write(data)
        world_file.close()
        self.logs.write("fini")

    def charge_from_file(self):  # charge les index à partir du fichier de monde
        world_file = open(DEFAULT_WORLD_FILE, "br")
        size = int.from_bytes(world_file.read(4), "big", signed=False)
        for index in range(size):
            self.chunks_index[(int.from_bytes(world_file.read(4), "big"), int.from_bytes(world_file.read(4), "big"), int.from_bytes(world_file.read(4), "big"))] = int.from_bytes(world_file.read(4), "big")
