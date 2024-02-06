import sqlite3
from datetime import datetime, timedelta

def init_DB(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS url (id INTEGER, link TEXT,create_at DATETIME, expire_at DATETIME)")

def inser_new_link(link) :

    # Récupération de résultat du Hash de Sabri
    id = "RESULTAT SABRI"

    # Lien d'origine
    link = link

    # Récupérer la date du jour
    create_at = datetime.now()

    # Ajouter 6 mois à la date actuelle
    expire_at = create_at + timedelta(days=30 * 6)

    print(f"Résultat : {id} - {link} - Date de création : {create_at} - Date d'expiration : {expire_at}")

    # cursor.execute("INSERT INTO url VALUES (id, link, create_at, expire_at)")

def delete_old_link():
    

if __name__ == "__main__":
    connection = sqlite3.connect("urlshortener.db")
    print(connection.total_changes)

    if connection.total_changes == 0 :
        print("Connexion OK")
    else :
        print("Connexion KO")

    cursor = connection.cursor()

    init_DB(cursor)

    inser_new_link("https://example.com")

