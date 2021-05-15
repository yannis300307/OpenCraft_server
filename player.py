from entity import Entity
from config import DEFAULT_SPAWN_POS, DEFAULT_DIR, CHUNK_SIZE, SERVER_NAME
from packets_send import KickPacket, RemoveEntityPacket, ChunkUpdatePacket
from chunk import Chunk

class Player(Entity):
    """Représente un joueur"""
    def __init__(self, id_: int, name: "", view_distance: int, client, world, tcp_clients, logs, noise):
        self.tcp_clients = tcp_clients
        self.noise = noise
        self.world = world
        self.logs = logs
        self.pos = list(DEFAULT_SPAWN_POS)
        self.name = name
        super().__init__(self.pos, "player", id_, DEFAULT_DIR, 20, tcp_clients, self.name)
        self.view_distance = view_distance
        self.client2 = client
        self.past_chunk_pos = (None, None, None)
        self.past_chunks = []

    def load_chunks(self):  # charge les chunks dans une zone donnée
        tpos = (int(self.pos[0]/CHUNK_SIZE), int(self.pos[1]/CHUNK_SIZE), int(self.pos[2]/CHUNK_SIZE))
        if tpos != self.past_chunk_pos:
            self.past_chunks = self.world.load_chunks_surroundings(self.pos, self.view_distance, self.client2, self.past_chunks)
            self.past_chunk_pos = tpos

    def load_chunks_loop(self):  # loop qui charge les chunks
        while self.client2 in self.tcp_clients:
            self.load_chunks()

    def kick(self, reason, send_message=True):  # kick le joueur
        packet = KickPacket(reason)
        packet2 = RemoveEntityPacket(self)
        packet.send_to(self)
        packet2.send_to(self)
        if send_message:
            self.client2.tchat.send_all("Déconnexion de " + self.name + ".", self)
        if self.name != SERVER_NAME:
            self.client2.close()

    def del_chunks(self, chunks_):
        for chunks in chunks_:
            packet = ChunkUpdatePacket(Chunk(chunks, self.noise))
            packet.send_to(self)
