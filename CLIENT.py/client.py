
import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection('51.210.112.107', 12345)

    # Message à envoyer au serveur
    message = 'imei:864893038636224,tracker,240918111525,,F,111525.00,A,0025.46333,N,00927.60696,E,31.162,106.68;'
    print(f'Envoi: {message}')
    writer.write(message.encode())
    await writer.drain()  # Assure que les données sont envoyées

    # Lecture de la réponse du serveur
    data = await reader.read(100)
    print(f'Reçu: {data.decode()}')

    # Fermer la connexion
    print('Fermeture de la connexion')
    writer.close()
    await writer.wait_closed()

# Exécuter le client
asyncio.run(tcp_client())


