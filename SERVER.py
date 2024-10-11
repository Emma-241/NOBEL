# main.py
import asyncio
from Decoder_messages import decode_tracker_data
from db_handler import init_db, save_to_db

HOST = "127.0.0.1"
PORT = 12345

async def handle_client(reader, writer):
    data = await reader.read(100)  # Lire jusqu'à 100 octets
    message = data.decode()
    print(f"Reçu du client: {message}")

    # Décoder les données du trackeur
    decoded_data = decode_tracker_data(message)
    if decoded_data:
        # Sauvegarder les données dans la base de données
        save_to_db(decoded_data)
        response = f"Données enregistrées: {decoded_data}"
    else:
        response = "Données non valides."

    writer.write(response.encode())
    await writer.drain()
    print(f"Envoyé au client: {response}")

async def main():
    init_db()  # Initialiser la base de données
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Serveur en écoute sur {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

asyncio.run(main())

print("end program")

"""ip :51.210.112.107
    Port 12345                     62354"""

