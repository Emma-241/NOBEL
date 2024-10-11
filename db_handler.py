import sqlite3

        # Fonction d'initialisation de la base de données

def init_db():
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

def save_to_db(data):
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tracking_data (imei, date, gps_fix, time, status, latitude_ns, longitude_ew)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['IMEI'], data['DATE'], data['GPS_FIX'], data['TIME'], data['STATUS'], data['LATITUDE_NS'], data['LONGITUDE_EW']))
    conn.commit()
    conn.close()

    print("Données enregistrées dans la base de données.")  #  Confirmation


    """cursor.execute('''
            INSERT INTO tracking_data (imei, date, gps_fix, time, status, latitude_ns, longitude_ew)
            VALUES (:imei, : date,:gps_fix,:time,:status,:latitude_ns,:longitude_ew ?)
        ''')"""
