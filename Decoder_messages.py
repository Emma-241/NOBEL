import re

# Regex pour les données du trackeur et le ping
PATTERN = r'imei:(?P<IMEI>[0-9]+),([a-z]+),(?P<DATE>\d{6})\d{6},,(?P<GPS_FIX>[FL]),(?P<TIME>\d{6})\.\d+,(?P<STATUS>[AV]),(\d+\.\d+),(?P<LATITUDE_NS>[NS]),(\d+\.\d+),(?P<LONGITUDE_EW>[ES]),(\d+\.\d+),(\d+\.\d+)'
PNG = r'^(?P<PING>\d{10,20})$'  # Nouvelle regex plus souple pour le ping


def decode_tracker_data(data):
    """Applique la regex sur les données du trackeur et retourne les résultats."""
    # Vérifie d'abord si le message est un ping
    PNG_match = re.match(PNG, data)
    if PNG_match:
        return {"action": "PING", "groups": PNG_match.group("PING")}

    # Si ce n'est pas un ping, vérifie si cela correspond aux données de tracking complètes
    match = re.match(PATTERN, data)
    if match:
        return match.groupdict()  # Retourne un dictionnaire avec les données extraites

    # Si aucune correspondance, retourne None
    return None
