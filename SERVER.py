import socket

# Paramètres du serveur
Host = "127.0.0.1"
Port = 62354
# Création du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Lier le socket à l'adresse IP et au port
server_socket.bind((Host, Port))

# Mettre le serveur en écoute (1 client max)
server_socket.listen(1)

print("En attente de connexion...")
# Le script s'arrête jusqu'à une connexion
client_socket, ip = server_socket.accept()
print(f"Le client ayant l'adresse IP",ip, "s'est connecté.")

while True:
    # Réception de la requête du client
    requete_client = client_socket.recv(500)
    requete_client = requete_client.decode("utf-8")

    if not requete_client:  # La connexion est interrompue
        print("Connexion interrompue.")
        break
    # Automatisation de la réponse du serveur
    if "Bonjour" in requete_client.lower():
        response = "Salut, comment puis-je vous aider ?"
    elif requete_client.isnumeric():
        num_recu = int(requete_client)
        response = str(pow(num_recu, 2,mod=2))

    else:
        response = "Message reçu !!!"


    # Envoyer la réponse au client
    client_socket.send(response.encode("utf-8"))

    # Affichage du message reçu du client
    print("Client:", requete_client)


# Fermer la connexion
client_socket.close()
server_socket.close()