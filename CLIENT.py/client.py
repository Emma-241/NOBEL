import socket
# Paramètres du serveur
Host = "127.0.0.1"
Port = 62354

# Création du socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client_socket.connect((Host, Port))

while True:
    # Saisir le message à envoyer
    msg = input("--> ")
    msg = msg.encode("utf-8")
    client_socket.send(msg)

    # Recevoir la réponse du serveur
    requete_server = client_socket.recv(500)
    requete_server = requete_server.decode('utf-8')
    print("Serveur:", requete_server)







