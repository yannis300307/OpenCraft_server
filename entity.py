from packets_send import SpawnEntityPacket, EntityMovementPacket, RemoveEntityPacket


class Entity:
    """représente une entitée"""
    def __init__(self, pos: (float, float, float), type_: str, id_: int, dir_: (int, int), maxlife: int, tcp_clients,
                 name: str = ""):
        self.tcp_clients = tcp_clients
        self.pos = list(pos)
        self.type = type_
        self.id = id_
        self.dir = list(dir_)
        self.max_life = maxlife
        self.name = name
        self.life = maxlife
        self.is_spawned = False

    def spawn(self):  # fait apparaitre l'entitée dans le monde
        self.is_spawned = True
        packet = SpawnEntityPacket(self)
        for client in self.tcp_clients:
            if self != client:
                packet.send_to(client)

    def get_pos(self):  # retourne la position dans le monde
        return self.pos

    def set_pos(self, pos: (float, float, float), dir_: (float, float) = None, imperative=False):  # change la position de l'entitée
        self.pos = tuple(pos)
        if dir_:
            self.dir = dir_
        packet = EntityMovementPacket(self, imperative)
        for client in self.tcp_clients:
            if client.id != self.id or imperative:
                packet.send_to(client)

    def despawn_entity(self):  # fait disparaitre l'entitée du monde
        packet = RemoveEntityPacket(self)
        for client in self.tcp_clients:
            if client.id != self.id:
                packet.send_to(client)
