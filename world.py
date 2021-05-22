from chunk import Chunk
from utils import *
from packets_send import ChunkUpdatePacket, SpawnEntityPacket, BlockUpdatePacket
from perlin_noise import PerlinNoise

class World:
    """Représente le monde"""
    def __init__(self, tcp_clients, noise, logs):
        self.noise = noise
        self.tcp_clients = tcp_clients
        self.chunks = {}
        self.entities = {}
        self.logs = logs
        self.chunks_indexes = {}
        self.last_id = 0
        self.noise2 = PerlinNoise(octaves=6, seed=SEED)
        self.charge_from_file()

    def get_chunk_in_pos(self, pos: (), addx=0, addy=0, addz=0):  # retourne le chunk à la position donnée
        tpos = (to_chunk(pos[0])+addx, to_chunk(pos[1])+addy, to_chunk(pos[2])+addz)
        ret = self.chunks.get(
            tpos)
        if ret is None:
            world_file = open(DEFAULT_WORLD_FILE, "br")
            size = int.from_bytes(world_file.read(4), "big")
            chunks = world_file.read()[size*16:]
            pos_ = (to_chunk(pos[0])+addx, to_chunk(pos[1])+addy, to_chunk(pos[2])+addz)
            if pos_ in list(self.chunks_indexes.keys()):
                chunk = chunks[self.chunks_indexes[pos_] * BLOCKS_FOR_CHUNK: self.chunks_indexes[pos_] * BLOCKS_FOR_CHUNK + BLOCKS_FOR_CHUNK]
                chunk_ = Chunk(pos_, self.noise, self)
                for block_ in range(len(chunk)):
                    chunk_.blocks[block_].type = BLOCKS_ID[chunk[block_]]
                ret = chunk_
        if ret is None:
            self.chunks[tpos] = Chunk(tpos, self.noise, self)
            self.chunks_indexes[tpos] = len(self.chunks_indexes) + 1
            chunk = self.chunks[tpos]
            chunk.gen_chunk()
            ret = chunk
        return ret

    def load_chunks_surroundings(self, pos: (), distance: int, client, charged_chunks):  # charge les chunks alentours et les envoi au client donné
        chunk_charged = 0
        chunks = []
        for y in range(-distance, min(distance, ceil_of_multiple(pos[1], 16))):
            for x in range(-distance, distance):
                for z in range(-distance, distance):
                    if client.connected:
                        tpos = (to_chunk(pos[0])+x, to_chunk(pos[1])+y, to_chunk(pos[2])+z)
                        if not tpos in charged_chunks:
                            chunk = self.get_chunk_in_pos(pos, x, y, z)
                            self.logs.write(
                                "Chargement du chuk à la position x=" + str(x) + " y=" + str(y) + " z=" + str(z),
                                print_=False)
                            chunk_charged += 1
                            if not chunk.trees_generated:
                                self.gen_trees(tpos)
                            if not chunk.is_empty():
                                packet = ChunkUpdatePacket(chunk)
                                packet.send_to(client)
                        chunks.append(tpos)
                    else:
                        return
        return chunks

    def set_block(self, pos, type_, clientt=None):
        chunk = self.get_chunk_in_pos(pos, 0, 0, 0)
        if chunk is not None:
            block = self.get_block(pos)
            block.type = type_
            packet = BlockUpdatePacket(block)
            for client in self.tcp_clients:
                if client != clientt:
                    packet.send_to(client)

    def get_block(self, pos: (int, int, int)):
        chunk = self.get_chunk_in_pos(pos, 0, 0, 0)
        return chunk.get_block((to_local(pos[0]), to_local(pos[1]), to_local(pos[2])))

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

    def gen_trees(self, chunks_zone: (int, int, int)):
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                block_pos = (x + CHUNK_SIZE * chunks_zone[0],
                             int(self.chunks[chunks_zone].heights_map[z * CHUNK_SIZE + x]),
                             z + CHUNK_SIZE * chunks_zone[2])
                if self.get_block(block_pos).type == "grass":
                    map_ = (self.noise2([(chunks_zone[0] * 16 + x) / CHUNK_SIZE, (chunks_zone[2] * 16 + z) / CHUNK_SIZE]) + 1)
                    if map_ > 1.5:
                        self.set_block((block_pos[0], block_pos[1] + 1, block_pos[2]), "stone")
                        self.set_block((block_pos[0], block_pos[1] + 2, block_pos[2]), "stone")
                        self.set_block((block_pos[0], block_pos[1] + 3, block_pos[2]), "stone")
                        self.set_block((block_pos[0], block_pos[1] + 4, block_pos[2]), "stone")
                        self.set_block((block_pos[0], block_pos[1] + 5, block_pos[2]), "stone")
                        self.set_block((block_pos[0], block_pos[1] + 6, block_pos[2]), "grass")
                        self.set_block((block_pos[0], block_pos[1] + 6, block_pos[2] + 1), "grass")
                        self.set_block((block_pos[0], block_pos[1] + 6, block_pos[2] - 1), "grass")
                        self.set_block((block_pos[0] + 1, block_pos[1] + 6, block_pos[2]), "grass")
                        self.set_block((block_pos[0] - 1, block_pos[1] + 6, block_pos[2]), "grass")
                        self.set_block((block_pos[0] + 1, block_pos[1] + 6, block_pos[2] + 1), "grass")
                        self.set_block((block_pos[0] - 1, block_pos[1] + 6, block_pos[2] - 1), "grass")
                        self.set_block((block_pos[0] + 1, block_pos[1] + 6, block_pos[2] - 1), "grass")
                        self.set_block((block_pos[0] - 1, block_pos[1] + 6, block_pos[2] + 1), "grass")

    def save(self):
        self.logs.write("Enregistrement du monde...")
        data = b""
        data += len(list(self.chunks.values())).to_bytes(4, "big", signed=False)
        pos_list = list(self.chunks.keys())
        index = 0
        self.logs.write("Ajout des indexs...")
        for chunk in pos_list:
            # data += chunk[0].to_bytes(4, "big", signed=True)
            # data += chunk[1].to_bytes(4, "big", signed=True)
            # data += chunk[2].to_bytes(4, "big", signed=True)
            # data += index.to_bytes(4, "big", signed=False)
            # index += 1
            self.save_chunk(chunk)
        # self.logs.write("Ajout des chunks...")
        # for chunk in pos_list:
        #     data += self.chunks[chunk].get_bytes_array()
        # self.logs.write("Enregistrement dans le fichier de sauvegarde du monde ...")
        # world_file = open(DEFAULT_WORLD_FILE, "bw")
        # world_file.write(data)
        # world_file.close()
        self.logs.write("fini")

    def charge_from_file(self):  # charge les index à partir du fichier de monde
        world_file = open(DEFAULT_WORLD_FILE, "br")
        size = int.from_bytes(world_file.read(4), "big", signed=False)
        for index in range(size):
            x = int.from_bytes(world_file.read(4), "big", signed=True)
            y = int.from_bytes(world_file.read(4), "big", signed=True)
            z = int.from_bytes(world_file.read(4), "big", signed=True)
            index_ = int.from_bytes(world_file.read(4), "big", signed=False)
            self.chunks_indexes[(x, y, z)] = index_

    def save_chunk(self, chunk):
        world_file = open(DEFAULT_WORLD_FILE, "br")
        if self.chunks[chunk].pos in self.chunks_indexes:
            data = world_file.read()
            world_file.close()
            start = len(self.chunks_indexes)*16 + 4
            datapast = data[:start+self.chunks_indexes[self.chunks[chunk].pos]*BLOCKS_FOR_CHUNK]
            datanext = data[start+self.chunks_indexes[self.chunks[chunk].pos]*BLOCKS_FOR_CHUNK+BLOCKS_FOR_CHUNK:]
            data = self.chunks[chunk].get_bytes_array().join([datapast, datanext])
            world_file = open(DEFAULT_WORLD_FILE, "bw")
            world_file.write(data)
            world_file.close()
        else:
            self.chunks_indexes[self.chunks[chunk].pos] = len(self.chunks_indexes) + 1
            data = world_file.read()
            pastdata = data[:int.from_bytes(data[:4], "big")*16]
            next_data = data[int.from_bytes(data[:4], "big")*16:]
            world_file.close()
            world_file = open(DEFAULT_WORLD_FILE, "wb")
            data = self.chunks[chunk].pos[0].to_bytes(4, "big", signed=True) + self.chunks[chunk].pos[1].to_bytes(4, "big", signed=True) + self.chunks[chunk].pos[2].to_bytes(4, "big", signed=True) + len(self.chunks_indexes).to_bytes(4, "big", signed=False)
            world_file.write(data.join([pastdata, next_data]))
            world_file.close()
            start = len(self.chunks_indexes) * 16 + 4
            datapast = data[:start + self.chunks_indexes[self.chunks[chunk].pos] * BLOCKS_FOR_CHUNK]
            datanext = data[start + self.chunks_indexes[self.chunks[chunk].pos] * BLOCKS_FOR_CHUNK + BLOCKS_FOR_CHUNK:]
            data = self.chunks[chunk].get_bytes_array().join([datapast, datanext])
            world_file = open(DEFAULT_WORLD_FILE, "bw")
            world_file.write(data)
            world_file.close()

