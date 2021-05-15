from config import *

class Block:
    """Représente un bloc"""
    def __init__(self, localpos: (int, int, int), globalpos: (int, int, int), nbt: {}):
        self.type = "air"
        self.localpos = localpos
        self.nbt = nbt
        self.globalpos = globalpos

    def get_localpos(self):  # donne la position dans le chunk
        return self.localpos

    def get_pos(self):  # donne la position dans le monde
        return self.globalpos

    def gen_bloc(self, height_map: list):  # génère le bloc avec le bruit de perlin
        noise_ = height_map[self.localpos[2]*CHUNK_SIZE+self.localpos[0]]
        if noise_ >= self.globalpos[1]:
            if noise_ - self.globalpos[1] <= GRASS_HEIGHT:
                self.type = "grass"
            elif noise_ - self.globalpos[1] <= DIRT_HEIGHT:
                self.type = "dirt"
            else:
                self.type = "stone"

    def get_nbt(self):  # donne les nbt
        return self.nbt

    def get_id(self):  # donne l'id du type
        return BLOCKS[self.type]

    def set_nbt(self, value: {}):  # change les nbt
        self.nbt = value