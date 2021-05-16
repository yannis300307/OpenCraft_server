from player import Player
from utils import *
from packets_send import *
from packets_manager import ReadPacket
from threading import Thread
from command import command


class Client(Player):
    """représente un client"""

    def __init__(self, tcp_client: (), world, logs, udp_clients, tcp_clients, tchat, udp, tcp, noise):
        self.tcp = tcp
        self.udp = udp
        self.tcp_clients = tcp_clients
        self.logs = logs
        self.udp_clients = udp_clients
        self.tchat = tchat
        self.world = world
        self.client = tcp_client
        self.view_distance = 3
        self.udp_client = ()
        self.temp_block = ()
        self.connected = True
        self.last_valid_pos = DEFAULT_SPAWN_POS
        id_ = get_new_id(world.last_id)
        world.last_id = id_
        if self.client is not None:
            super().__init__(id_, self.get_client_socket()[1][0] + ": " + str(self.get_client_socket()[1][1]),
                             self.view_distance, self, self.world, self.tcp_clients, logs, noise)
        else:
            super().__init__(id_, "None", self.view_distance, self, self.world, self.tcp_clients, logs, noise)
        self.world.entities[self.id] = self

    def connect_client(self, name: str, view_distance: int):  # set la distance de vue et le nom
        self.name = name
        self.view_distance = view_distance

    def spawn_player(self):  # fait apparaitre le joueur dans le monde
        self.spawn()
        packet = JoinWorldPacket()
        packet.send_to(self)

    def get_client_socket(self):  # retourne le socket tcp du client
        return self.client

    def bind_udp(self, udp_client):  # lie le client tcp et udp
        self.udp_client = udp_client
        self.udp_clients[udp_client] = self

    def send(self, bytes_: bytes, udp_=False):  # permet d'envoyer un packet
        if self.client is not None:
            try:
                if udp_:
                    self.udp.sendto(bytes_, self.udp_client)
                else:
                    self.client[0].send(bytes_)
            except:
                self.connected = False
                try:
                    self.tcp_clients.remove(self)
                except ValueError:
                    pass
                self.logs.write("Déconnection de " + self.get_client_socket()[1][0] + ": " + str(
                    self.get_client_socket()[1][1]))

    def listen_tcp(self):  # analise les packets envoyés par le client
        while True:
            try:
                brut = self.get_client_socket()[0].recv(1)
                if brut not in [b""]:
                    packet_type = int.from_bytes(brut, "big")
                    if packet_type == 0:
                        packet = ReadPacket(self)
                        self.connect_client(packet.read_string(), packet.read_int())
                        self.udp_client = (self.get_client_socket()[1][0], packet.read_int())
                        self.udp_clients[self.udp_client] = self
                        del packet
                        for car in self.name:
                            if not car in CHARACTERS_FOR_NAME:
                                self.kick("Caractère(s) invalide(s).")
                        if len(self.name) > 10:
                            self.kick("Le pseudo dépasse la taille maximum.")
                        elif len(self.name) < 3:
                            self.kick("Le pseudo est trop court")
                        for client in self.tcp_clients:
                            if client != self:
                                if client.name.lower() == self.name.lower():
                                    self.kick("Quelqu'un a déjà prit ce nom !")
                        packet = LoginSuccessPacket(self)
                        packet.send_to(self)
                        self.load_chunks()
                        self.spawn_player()
                        self.world.spawn_entities(self)
                        Thread(target=self.load_chunks_loop).start()
                    elif packet_type == 1:
                        self.despawn_entity()
                        self.tcp_clients.remove(self)
                        self.close()
                        self.logs.write("Déconnection de " + self.get_client_socket()[1][0] + ": " + str(
                            self.get_client_socket()[1][1]))
                        del packet
                        break
                    elif packet_type == 3:
                        packet = ReadPacket(self)
                        msg = packet.read_string()
                        if msg.startswith("/"):
                            command(msg, self.tcp_clients, self.logs, self.tcp, self.udp, self, self.tchat, self.world)
                        else:
                            self.tchat.send_all(msg, self)
                        del packet
                    elif packet_type == 4:
                        packet = ReadPacket(self)
                        x, y, z = packet.read_int(), packet.read_int(), packet.read_int()
                        self.temp_block = (x, y, z)
                    elif packet_type == 5:
                        self.temp_block = ()
                    elif packet_type == 6:
                        self.world.set_block(self.temp_block, "air", self)
                    elif packet_type == 7:
                        packet = ReadPacket(self)
                        self.world.set_block((packet.read_int(), packet.read_int(), packet.read_int()), BLOCKS_ID[packet.read_byte()], self)
                else:
                    self.despawn_entity()
                    self.tcp_clients.remove(self)
                    try:
                        del self.udp_clients[self.udp_client]
                    except KeyError:
                        pass
                    self.logs.write("Déconnection de " + self.get_client_socket()[1][0] + ": " + str(
                        self.get_client_socket()[1][1]))
                    return
            except:
                self.despawn_entity()
                try:
                    self.tcp_clients.remove(self)
                    del self.udp_clients[self.udp_client]
                except ValueError:
                    pass
                self.logs.write(
                    "Déconnection de " + self.get_client_socket()[1][0] + ": " + str(
                        self.get_client_socket()[1][1]))
                return

    def close(self):  # ferme la conection avec le client
        self.client[0].close()
