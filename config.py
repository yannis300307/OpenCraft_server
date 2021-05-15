# fichier contenant les constantes nécéssaires et modifiables

DEFAULT_LOGS_PATH = "logs"

CHUNK_SIZE = 16

FLOOR_HEIGHT = 100
MIN_FLOOR_HEIGHT = 70

GRASS_HEIGHT = 1
DIRT_HEIGHT = 5

BLOCKS_FOR_CHUNK = CHUNK_SIZE**3

BLOCKS = {"air": 0, "stone": 1, "dirt": 2, "grass": 3}
ENTITIES = {"player": 0}

DEFAULT_SPAWN_POS = (0.0, 50.0, 0.0)
DEFAULT_SPAWN_DIR = (0.0, 0.0)

DEFAULT_DIR = (0.0, 0.0)

SEED = 28

DEFAULT_WORLD_FILE = "world.OpenWorld"

SERVER_NAME = "SERVEUR"
