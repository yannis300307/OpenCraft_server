from config import *
from block import Block
from utils import to_chunk

class Chunk:
    """Représente un chunk"""
    def __init__(self, pos: (int, int, int), noise, world):
        self.noise = noise
        self.blocks = [None for _ in range(CHUNK_SIZE ** 3)]
        self.blocks = list(self.blocks)
        self.world = world
        for y in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    self.blocks[z * CHUNK_SIZE ** 2 + y * CHUNK_SIZE + x] = Block((x, y, z), (pos[0]*CHUNK_SIZE+x, pos[1]*CHUNK_SIZE+y, pos[2]*CHUNK_SIZE+z), {})
        self.pos = pos
        self.heights_map = self.gen_heights_map()

    def gen_chunk(self):  # génère le chunk avec le bruit de perlin
        for block in self.blocks:
            block.gen_bloc(self.heights_map)

    def get_block(self, pos: (int, int, int)):  # donne le bloc demandé
        return self.blocks[pos[2] * (CHUNK_SIZE ** 2) + pos[1] * CHUNK_SIZE + pos[0]]

    def get_all_blocks(self):  # donne tous les blocs
        return self.blocks

    def get_pos(self):  # donne la position du chunk dans le monde
        return self.pos

    def is_empty(self):  # retourn True si le chunl est vide (remplit d'air)
        for block in self.blocks:
            if block.type != "air":
                return False
        return True

    def get_bytes_array(self):  # donne une liste de bytes contennant tous les blocs du chunk
        bytes_list = b""
        for block in self.blocks:
            bytes_list += block.get_id().to_bytes(1, "big", signed=False)
        return bytes_list

    def gen_heights_map(self):  # génère un heights_map généré par le bruit de perlin qui est utilisée pour générer le chunk
        heights = [0 for _ in range(CHUNK_SIZE ** 2)]
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                heights[z*CHUNK_SIZE+x] = (self.noise([(self.pos[0]*16+x)/CHUNK_SIZE, (self.pos[2]*16+z)/CHUNK_SIZE])+1)*WORLD_AMPLIFICATION
        return heights
