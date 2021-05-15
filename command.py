import sys

from config import SERVER_NAME


def command(cmd, tcp_clients, logs, tcp, udp, clientt, tchat, world):  # gère les commandes
    tcmd = cmd.split()
    if type(clientt) != str:
        client_name = clientt.name
    else:
        client_name = clientt
    if tcmd[0] == "/tp":
        logs.write("Commande /tp utilisée par " + client_name + ".")
        if len(tcmd) == 5 or len(tcmd) == 7:
            find = False
            for client in tcp_clients:
                if client.name.lower() == tcmd[1].lower():
                    try:
                        if len(tcmd) == 5:
                            client.set_pos((float(tcmd[2]), float(tcmd[3]), float(tcmd[4])), imperative=True)
                            logs.write("Téléportation de " + client.name + " en x=" + tcmd[2] + " y=" + tcmd[3] + " z=" + tcmd[4])
                        else:
                            client.set_pos((float(tcmd[2]), float(tcmd[3]), float(tcmd[4])), (float(tcmd[5]), float(tcmd[6])), imperative=True)
                            logs.write(
                                "Téléportation de " + client.name + " en x=" + tcmd[2] + " y=" + tcmd[3] + " z=" + tcmd[4] + " pitch=" + tcmd[5], " yaw=" + tcmd[6])
                    except ValueError:
                        logs.write("Argument(s) invalide(s).")
                    find = True
                    break
            if not find:
                logs.write("Joueur " + tcmd[1] + " non trouvé.")
        elif len(tcmd) < 5:
            logs.write("Argument(s) manquant(s) :")
            logs.write("/tp [pseudo] [x] [y] [z] {[pitch] [yaw]}")
    elif tcmd[0] == "/stop":
        logs.write("Commande /stop utilisée par " + client_name + ".")
        if len(tcmd) == 1:
            logs.write("Fermeture du serveur...")
            for client in tcp_clients:
                client.kick("Serveur fermé", send_message=False)
            tcp.close()
            udp.close()
            world.save()
            logs.write("éteint.")
            sys.exit()
        else:
            logs.write("Aucun argument n'est attendu.")
    elif tcmd[0] == "/kick":
        logs.write("Commande /kick utilisée par " + client_name + ".")
        if len(tcmd) > 2:
            find = False
            for client in tcp_clients:
                if client.name.lower() == tcmd[1].lower():
                    if client.name != SERVER_NAME:
                        client.kick(" ".join(tcmd[2:]), send_message=False)
                        logs.write("Joueur " + tcmd[1] + " a été kické.")
                        find = True
                        break
            if not find:
                logs.write("Joueur " + tcmd[1] + " non trouvé.")
        else:
            logs.write("Argument(s) manquant(s) :")
            logs.write("/kick [pseudo] **[message]**")
    elif tcmd[0] == "/msg":
        logs.write("Commande /msg utilisée par " + client_name + ".")
        if len(tcmd) > 2:
            find = False
            for client in tcp_clients:
                if client.name.lower() == tcmd[1].lower():
                    tchat.send_to(" ".join(tcmd[2:]), client, clientt)
                    find = True
                    break
            if not find:
                logs.write("Joueur " + tcmd[1] + " non trouvé.")
        else:
            logs.write("Argument(s) manquant(s) :")
            logs.write("/msg [pseudo] **[message]**")
    elif tcmd[0] == "/playerlist":
        logs.write("Commande /msg utilisée par " + client_name + ".")
        if len(tcmd) == 1:
            if len(tcp_clients) >= 1:
                for client in tcp_clients:
                    logs.write("- nom: " + client.name + ", ip/port: " + client.get_client_socket()[1][0] + ": " + str(client.get_client_socket()[1][1]))
            else:
                logs.write("Aucun joueur n'est connecté.")
        else:
            logs.write("Aucun argument n'est attendu.")
    elif tcmd[0] == "/getpos":
        if len(tcmd) == 2:
            find = False
            for client in tcp_clients:
                if client.name.lower() == tcmd[1].lower():
                    logs.write(tcmd[1] + " se trouve en x=" + str(client.pos[0]) + " y=" + str(client.pos[1]) + " z=" + str(client.pos[2]) + " pitch=" + str(client.dir[0]) + " yaw=" + str(client.dir[1]))
                    find = True
                    break
            if not find:
                logs.write("Joueur " + tcmd[1] + " non trouvé.")
    elif tcmd[0] == "/purgechunks":
        if len(tcmd) == 1:
            logs.write("Rechargement des chunks ...")
            past_pos = {}
            logs.write("Copie des positions...")
            for client in tcp_clients:
                past_pos[client] = client.pos
            logs.write("Supression des chunks...")
            world.chunks = {}
            for client in tcp_clients:
                client.past_chunk_pos = (None, None, None)
                tpast_chunks = client.past_chunks
                client.past_chunks = []
                client.del_chunks(tpast_chunks)
            logs.write("Chargement des chunks...")
            for client in tcp_clients:
                client.load_chunks()
                client.set_pos(past_pos[client], imperative=True)
            logs.write("fini")
    else:
        logs.write("Commande " + tcmd[0] + " inconnue !")
