import math
from config import *


# fonctions de calcule utiles

def invert_bytes(bytes__):  # inverse les bytes arrays
    bytes_ = b""
    for byte in range(len(bytes__)):
        bytes_ += bytes__[len(bytes__) - 1 - byte].to_bytes(1, "big")
    return bytes_

def get_new_id(last_id):  # génère une nouvelle id
    last_id += 1
    return last_id

def ceil_of_multiple(nbr, multiple):  # donne le plafond du multiple
    return math.ceil(nbr / multiple) * multiple


def floor_of_multiple(nbr, multiple):  # donne le sol du multiple
    return math.floor(nbr / -multiple) * multiple


def get_distance(pos1: (), pos2: ()):  # donne la distance 3D
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)

def to_block(v: float):
    return int(math.floor(v))

def to_chunk(v):
    return to_block(float(v)/CHUNK_SIZE)

def to_local(v):
    return to_block(v) - (to_chunk(v) * CHUNK_SIZE)

def is_float(v):
    try:
        float(v)
        return True
    except ValueError:
        return False

def get_player_pos(p: str, pos_axis: int, start_pos):
    if p.startswith("~"):
        if p == "~":
            p = "~0"
        if is_float(p[1:]):
            pl_p = list(start_pos)
            pl_p[pos_axis] = start_pos[pos_axis] + float(p[1:])
            return float(pl_p[pos_axis])
    else:
        if is_float(p):
            return float(p)
