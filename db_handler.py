import sqlite3
from datetime import datetime
from passlib.context import CryptContext

# Contexte de hachage pour sécuriser les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
            latitude REAL,
            longitude REAL
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

    # Création de la table pour les utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            mot_de_passe TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables initialisées avec succès.")

# Fonction pour hacher un mot de passe
def hash_password(password):
    return pwd_context.hash(password)

# Fonction pour ajouter un utilisateur dans la base de données
def add_user(email, password):
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()

    # Hachage du mot de passe avant insertion
    hashed_password = hash_password(password)

    # Insertion de l'utilisateur dans la table 'users'
    try:
        cursor.execute("INSERT INTO users (email, mot_de_passe) VALUES (?,?)", (email, hashed_password))
        conn.commit()
        print("Nouvel utilisateur ajouté avec succès.")
    except sqlite3.IntegrityError:
        print("Erreur : un utilisateur avec cet email existe déjà.")
    finally:
        conn.close()

# Fonction pour sauvegarder les données du trackeur
def save_to_db(data):
    """Enregistre les données du trackeur décodées dans la base de données."""
    conn = sqlite3.connect('tracking_data.db')
    cursor = conn.cursor()

    # Insertion des données de tracking dans la table tracking_data
    cursor.execute('''
        INSERT INTO tracking_data (imei, date, gps_fix, time, status, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['IMEI'], data['DATE'], data['GPS_FIX'], data['TIME'], data['STATUS'], data['LATITUDE'], data['LONGITUDE']
    ))

    conn.commit()
    conn.close()
    print("Données enregistrées dans la table tracking_data.")

# Fonction pour sauvegarder un ping dans la table PING
def save_ping(imei):
    """Enregistre un ping pour un IMEI spécifique, avec mise à jour automatique."""
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
