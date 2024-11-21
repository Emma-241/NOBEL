import asyncio
from Decoder_messages import decode_tracker_data  # Fichier de décodage des données
from db_handler import init_db, save_to_db, save_ping  # Gestion de la base de données


class TrackerServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        # Initialiser la connexion avec le client
        peername = transport.get_extra_info('peername')
        print(f"Connexion établie avec {peername}")
        self.transport = transport

    def data_received(self, data):
        # Décoder les données reçues
        message = data.decode()
        print(f"Données reçues: {message}")

        # Décoder les données du tracker
        decoded_data = decode_tracker_data(message)

        if decoded_data:
            # Vérifier si le message est un ping
            if decoded_data.get("action") == "PING":
                imei = decoded_data["groups"]  # Accède à la valeur du ping par "groups"
                save_ping(imei)  # Enregistrer le ping dans la base
                response = "PING reçu et enregistré."
            else:
                # Sauvegarder les données de tracking dans la base de données
                save_to_db(decoded_data)
                response = f"Données enregistrées: {decoded_data}"
        else:
            response = "Données non valides."

        # Envoyer la réponse au client
        print(f"Envoi de la réponse: {response}")
        self.transport.write(response.encode())


async def main():
    # Initialiser la base de données une fois avant le démarrage du serveur
    init_db()

    # Obtenir la boucle d'événements actuelle
    loop = asyncio.get_running_loop()

    # Créer le serveur avec TrackerServerProtocol sur l'adresse IP spécifiée
    server = await loop.create_server(
        TrackerServerProtocol,
        '51.210.112.107', 12345
    )

    print("Serveur en écoute sur 51.210.112.107:12345")

    # Démarrer le serveur de manière asynchrone
    async with server:
        await server.serve_forever()


# Exécuter le serveur
asyncio.run(main())
