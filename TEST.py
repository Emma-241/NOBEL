import re

# Regex pour les données du trackeur et le ping
PATTERN = r'imei:(?P<IMEI>[0-9]+),([a-z]+),(?P<DATE>\d{6})\d{6},,(?P<GPS_FIX>[FL]),(?P<TIME>\d{6})\.\d+,(?P<STATUS>[AV]),(?P<LATITUDE>\d+\.\d+),(?P<LATITUDE_NS>[NS]),(?P<LONGITUDE>\d+\.\d+),(?P<LONGITUDE_EW>[EW]),(?P<SPEED>\d+\.\d+),(?P<ORIENTATION>\d+\.\d+)'
PNG = r'^(?P<PING>\d{10,20})$'  # Nouvelle regex plus souple pour le ping


def conversor_latitude_longitude(value, direction):
    """Convertit la latitude ou la longitude en degrés décimaux.

    Si la direction est 'N' ou 'S', elle utilise les 2 premiers chiffres comme degrés pour la latitude.
    Si la direction est 'E' ou 'W', elle utilise les 3 premiers chiffres pour la longitude.
    """
    if direction in ['N', 'S']:
        degrees = int(value[:2])  # 2 premiers chiffres pour la latitude
        minutes = float(value[2:]) / 60  # Divise le reste par 60 pour les minutes
    elif direction in ['E', 'W']:
        degrees = int(value[:3])  # 3 premiers chiffres pour la longitude
        minutes = float(value[3:]) / 60  # Divise le reste par 60 pour les minutes
    else:
        return None  # En cas d'erreur de direction

    # Combine degrés et minutes en degrés décimaux
    decimal_degrees = degrees + minutes
    # Si la direction est 'S' ou 'W', on utilise un signe négatif
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def decode_tracker_data(data):
    """Applique la regex sur les données du trackeur et retourne les résultats."""
    # Vérifie d'abord si le message est un ping
    PNG_match = re.match(PNG, data)
    if PNG_match:
        return {"action": "PING", "groups": PNG_match.group("PING")}

    # Si ce n'est pas un ping, vérifie si cela correspond aux données de tracking complètes
    match = re.match(PATTERN, data)
    if match:
        result = match.groupdict()

        # Convertit la latitude et la longitude en degrés décimaux
        latitude_decimal = conversor_latitude_longitude(result["LATITUDE"], result["LATITUDE"])
        longitude_decimal = conversor_latitude_longitude(result["LONGITUDE"], result["LONGITUDE"])

        # Ajoute les latitudes et longitudes converties dans le résultat
        result["LATITUDE_DECIMAL"] = latitude_decimal
        result["LONGITUDE_DECIMAL"] = longitude_decimal
        return result

    # Si aucune correspondance, retourne None
    return None


# Exemple d'utilisation avec votre donnée
data = "imei:864893038636224,tracker,240918111525,,F,111525.00,A,0025.46333,N,00927.60696,E,31.162,106.68"
decoded_data = decode_tracker_data(data)
print(decoded_data)

