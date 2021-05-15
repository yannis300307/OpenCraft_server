import socket
from threading import Thread
import perlin_noise
from logs import *
from tchat import Tchat
from world import World
from network_manager import accept_tcp, listen_udp
from command import command
from config import SERVER_NAME
import sys


def input_loop():  # Récupère les messages de la console
    while True:
        txt = input()
        if txt.startswith("/"):
            ret = command(txt, tcp_clients, logs, tcp, udp, SERVER_NAME, tchat, world)
            if ret == "stop":
                return
        else:
            tchat.send_all(txt, SERVER_NAME)


if __name__ == "__main__":  # main
    # initialise le serveur
    ip, port = "", 9322
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    logs = Logs()

    try:
        logs.write("fini")

        logs.write("Création du serveur ... ")

        tcp_clients = []
        udp_clients = {}

        noise = perlin_noise.PerlinNoise(octaves=1, seed=SEED)

        world = World(tcp_clients, noise, logs)

        tchat = Tchat(logs, tcp_clients)

        logs.write("fini")
        tcp.bind((ip, port))
        udp.bind((ip, port))
        tcp.listen()
        # lance les threads qui connectent les clients tcp et udp et lance input_loop
        Thread(target=lambda: accept_tcp(logs, tcp, tcp_clients, udp, tchat, udp_clients, world)).start()
        Thread(target=input_loop).start()
        Thread(target=lambda: listen_udp(udp, udp_clients, world)).start()
    except:
        # gère les exceoption et les écrit dans les logs
        logs.write(sys.exc_info()[0].__name__ + ": " + sys.exc_info()[1].args[0] + " | " + str(sys.exc_info()[2]))
