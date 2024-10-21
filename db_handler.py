import sqlite3
from datetime import datetime

# Fonction d'initialisation de la base de données
def init_db():
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()

    # Création de la table pour les données principales du trackeur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imei TEXT,
            date TEXT,
            gps_fix TEXT,
            time TEXT,
            status TEXT,
            latitude_ns TEXT,
            longitude_ew TEXT
        )
    ''')

    # Création de la table pour les pings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PING (
            imei TEXT PRIMARY KEY,
            num_pings INTEGER,
            last_ping TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Fonction pour sauvegarder les données du trackeur
def save_to_db(data):
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tracking_data (imei, date, gps_fix, time, status, latitude_ns, longitude_ew)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['IMEI'], data['DATE'], data['GPS_FIX'], data['TIME'], data['STATUS'], data['LATITUDE_NS'], data['LONGITUDE_EW']))
    conn.commit()
    conn.close()
    print("Données enregistrées dans la table tracking_data.")

# Fonction pour sauvegarder un ping dans la table PING
def save_ping(imei):
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()

    # Utiliser REPLACE pour insérer ou mettre à jour les informations de ping
    cursor.execute('''
        REPLACE INTO PING (imei, num_pings, last_ping)
        VALUES (
            ?,
            COALESCE((SELECT num_pings + 1 FROM PING WHERE imei = ?), 1),
            ?
        )
    ''', (imei, imei, datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print(f"Ping enregistré pour IMEI {imei} dans la table PING.")