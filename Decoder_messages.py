import re

# Regex pour les données du trackeur
PATTERN = r'imei:(?P<IMEI>[0-9]+),([a-z]+),(?P<DATE>\d{6})\d{6},,(?P<GPS_FIX>[FL]),(?P<TIME>\d{6})\.\d+,(?P<STATUS>[AV]),(\d+\.\d+),(?P<LATITUDE_NS>[NS]),(\d+\.\d+),(?P<LONGITUDE_EW>[ES]),(\d+\.\d+),(\d+\.\d+);'

def decode_tracker_data(data):
    """Applique la regex sur les données du trackeur et retourne les résultats."""
    match = re.match(PATTERN, data)
    if match:
        return match.groupdict()  # Retourne un dictionnaire avec les données extraites
    else:
        return None  # Retourne rien si le format est invalide

