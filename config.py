# fichier contenant les constantes nécéssaires et modifiables

DEFAULT_LOGS_PATH = "logs"

CHUNK_SIZE = 16

FLOOR_HEIGHT = 100
MIN_FLOOR_HEIGHT = 70

GRASS_HEIGHT = 1
DIRT_HEIGHT = 5

BLOCKS_FOR_CHUNK = CHUNK_SIZE**3

BLOCKS = {"air": 0, "stone": 1, "dirt": 2, "grass": 3}
BLOCKS_ID = {0: "air", 1: "stone", 2: "dirt", 3: "grass"}
ENTITIES = {"player": 0}


CARACTERES = "abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_&éèçà"

CHARACTERS_FOR_NAME = []

for c in CARACTERES:
    CHARACTERS_FOR_NAME.append(c)

DEFAULT_DIR = (0.0, 0.0)

SEED = 28
WORLD_AMPLIFICATION = 2
WORLD_OCTAVE = 1

DEFAULT_SPAWN_POS = (0.0, WORLD_AMPLIFICATION+GRASS_HEIGHT+DIRT_HEIGHT, 0.0)
DEFAULT_SPAWN_DIR = (0.0, 0.0)

DEFAULT_WORLD_FILE = "world.OpenWorld"

SERVER_NAME = "SERVEUR"
