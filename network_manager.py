from threading import Thread
from client import Client
from packets_manager import ReadUdpPacket
import math

def accept_tcp(logs, tcp, tcp_clients, udp, tchat, udp_clients, world, noise):  # connecte les clients tcp
    while True:
        logs.write("en attente ...")
        try:
            client = tcp.accept()
        except OSError:
            return
        clientt = Client(client, world, logs, udp_clients, tcp_clients, tchat, udp, tcp, noise)
        logs.write("Connection de " + client[1][0] + ": " + str(client[1][1]))
        tcp_clients.append(clientt)
        Thread(target=clientt.listen_tcp).start()


def listen_udp(udp, udp_clients, world):  # connecte les clients udp
    while True:
        try:
            data, client = udp.recvfrom(8192)
        except:
            return
        packet = ReadUdpPacket(data)
        packet_id = packet.read_byte()
        if packet_id == 2:
            if client in udp_clients:
                clientt: Client = udp_clients[client]
                pos = [0, 0, 0]
                pos[0] = packet.read_float()
                pos[1] = packet.read_float()
                pos[2] = packet.read_float()
                if not math.nan in pos:
                    clientt.set_pos(pos)
                clientt.dir[0] = packet.read_float()
                clientt.dir[1] = packet.read_float()
                world.update_entities(clientt.id, pos[0], pos[1], pos[2], clientt.dir[0], clientt.dir[1])
        del packet
