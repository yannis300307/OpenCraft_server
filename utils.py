import math

last_id = 0

# fonctions de calcule utiles

def invert_bytes(bytes__):  # inverse les bytes arrays
    bytes_ = b""
    for byte in range(len(bytes__)):
        bytes_ += bytes__[len(bytes__) - 1 - byte].to_bytes(1, "big")
    return bytes_

def get_new_id():  # génère une nouvelle id
    global last_id
    last_id += 1
    return last_id

def ceil_of_multiple(nbr, multiple):  # donne le plafond du multiple
    return math.ceil(nbr / multiple) * multiple


def floor_of_multiple(nbr, multiple):  # donne le sol du multiple
    return math.floor(nbr / -multiple) * multiple


def get_distance(pos1: (), pos2: ()):  # donne la distance 3D
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)
