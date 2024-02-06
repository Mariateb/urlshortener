# Save this as url_shortener_class.py
import sqlite3
from datetime import datetime, timedelta

class UrlShortener:
    def __init__(self, db_filename="urlshortener.db"):
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.init_DB()

    def init_DB(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS url (id INTEGER, link TEXT, create_at DATETIME, expire_at DATETIME)")

    def inser_new_link(self, link, days=180):
        # Récupération de résultat du Hash de Sabri
        id = "lol"

        # Lien d'origine
        link = link

        # Récupérer la date du jour
        create_at = datetime.now()

        # Ajouter la durée spécifiée en jours à la date actuelle
        expire_at = create_at + timedelta(days=days)

        print(f"Résultat : {id} - {link} - Date de création : {create_at} - Date d'expiration : {expire_at}")

        self.cursor.execute("INSERT INTO url VALUES (?, ?, ?, ?)", (id, link, create_at, expire_at))

    def delete_old_link(self):
        # Récupérer la date du jour
        current_date = datetime.now()

        # Sélectionner les liens expirés
        self.cursor.execute("SELECT id, link, create_at, expire_at FROM url WHERE expire_at <= ?", (current_date,))
        expired_links = self.cursor.fetchall()

        # Parcourir les liens expirés
        for link_data in expired_links:
            # Afficher les informations
            print(f"Expired Link - ID: {link_data[0]} - Link: {link_data[1]} - Create Date: {link_data[2]} - Expire Date: {link_data[3]}")

            # Supprimer le lien expiré de la base de données
            self.cursor.execute("DELETE FROM url WHERE id = ?", (link_data[0],))

    # Ajoutez cette méthode à la classe UrlShortener dans le fichier url_shortener_class.py

    def get_short_url(self, link_id):
        # Retrieve the link associated with the ID
        self.cursor.execute("SELECT link FROM url WHERE id = ?", (link_id,))
        result = self.cursor.fetchone()

        if result:
            link = result[0]
            short_url = f"urlshortener.fr/{link_id}"
            print(f"Short URL for ID {link_id}: {short_url} - Original Link: {link}")
            return short_url

        print(f"No link found for ID {link_id}")
        return None


    def close_connection(self):
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    url_shortener = UrlShortener()
    url_shortener.inser_new_link("https://example.com")
    url_shortener.delete_old_link()
    url_shortener.close_connection()
