
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


""" import re

data = "imei:864893038636224,tracker,240918111525,,F,111525.00,A,0025.46333,N,00927.60696,E,31.162,106.68;"

# Regex fournie des groupes nommés
pattern = r'imei:(?P<IMEI>[0-9]+),([a-z]+),(?P<DATE>\d{6})\d{6},,(?P<GPS_FIX>[FL]),(?P<TIME>\d{6})\.\d+,(?P<STATUS>[AV]),(\d+\.\d+),(?P<LATITUDE_NS>[NS]),(\d+\.\d+),(?P<LONGITUDE_EW>[ES]),(\d+\.\d+),(\d+\.\d+);'

# Appliquer la regex
match = re.match(pattern, data)
if match:
    resultat = match.groupdict()
    print(resultat)

else :
    print("entrée invalide")

print("End programme!!!")

print("finished") """
