# from main import logs, tcp_clients, server
from packets_send import ChatPacket
from config import SERVER_NAME

class Tchat:
    """Le tchat du jeu"""
    def __init__(self, logs, tcp_clients):
        self.msgs = []
        self.logs = logs
        self.tcp_clients = tcp_clients

    @staticmethod
    def __format_msg(msg: "", sender_name):  # formate le texte pour le tchat
        return "[" + sender_name + "] > " + msg

    def send_to(self, msg: "", receiver, sender, logs_=True):  # envoie un message à une personne
        if sender != SERVER_NAME:
            msg = self.__format_msg(msg, sender.name)
            if logs_:
                self.logs.write(sender.get_client_socket()[1][0] + ": " + str(sender.get_client_socket()[1][1]) + " > " + msg)
            packet = ChatPacket(msg)
            packet.send_to(receiver)
        else:
            msg = self.__format_msg(msg, SERVER_NAME)
            self.logs.write("Interne" + ": " + SERVER_NAME + " > " + msg)
            packet = ChatPacket(msg)
            packet.send_to(receiver)

    def send_all(self, msg: "", sender):  # envoie le message à tout le monde
        if sender != SERVER_NAME:
            self.logs.write(sender.get_client_socket()[1][0] + ": " + str(
                sender.get_client_socket()[1][1]) + " > " + self.__format_msg(msg, sender.name))
        else:
            self.logs.write("Interne > " + self.__format_msg(msg, sender))
        for client in self.tcp_clients:
            self.send_to(msg, client, sender, logs_=False)
