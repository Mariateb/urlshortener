# Sauvegardez ceci en tant que url_shortener_class.py
import sqlite3
from datetime import datetime, timedelta

class UrlShortener:
    """
    Une classe pour gérer les opérations de raccourcissement d'URL en utilisant SQLite comme backend de stockage.

    Attributs:
        connection (sqlite3.Connection): Connexion à la base de données SQLite.
        cursor (sqlite3.Cursor): Curseur de la base de données SQLite.

    Méthodes:
        __init__(self, db_filename="urlshortener.db"):
            Initialise une nouvelle instance de la classe UrlShortener.

        init_DB(self):
            Initialise la base de données SQLite en créant la table 'url' si elle n'existe pas.

        inser_new_link(self, link, days=180):
            Insère un nouveau lien dans la table 'url' avec une date d'expiration basée sur les jours fournis.

        delete_old_link(self):
            Supprime les liens expirés de la table 'url'.

        get_short_url(self, link_id):
            Récupère le lien d'origine associé à l'ID donné et génère une URL courte.

        close_connection(self):
            Valide les modifications et ferme la connexion à la base de données SQLite.

    Exemple d'utilisation:
        url_shortener = UrlShortener()
        url_shortener.inser_new_link("https://example.com")
        url_shortener.delete_old_link()
        url_shortener.close_connection()
    """

    def __init__(self, db_filename="urlshortener.db"):
        """
        Initialise une nouvelle instance de la classe UrlShortener.

        Paramètres:
            db_filename (str): Le nom de fichier de la base de données SQLite (par défaut, "urlshortener.db").
        """
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.init_DB()

    def init_DB(self):
        """
        Initialise la base de données SQLite en créant la table 'url' si elle n'existe pas.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS url (id INTEGER, link TEXT, create_at DATETIME, expire_at DATETIME)")

    def inser_new_link(self, link, days=180):
        """
        Insère un nouveau lien dans la table 'url' avec une date d'expiration basée sur les jours fournis.

        Paramètres:
            link (str): L'URL d'origine à raccourcir.
            days (int): Le nombre de jours jusqu'à l'expiration du lien (par défaut, 180).

        Retourne:
            int: L'ID attribué par la base de données pour le lien inséré.
        """
        id = "lol"
        link = link
        create_at = datetime.now()
        expire_at = create_at + timedelta(days=days)

        self.cursor.execute("INSERT INTO url VALUES (?, ?, ?, ?)", (id, link, create_at, expire_at))
        return self.cursor.lastrowid

    def delete_old_link(self):
        """
        Supprime les liens expirés de la table 'url'.
        """
        current_date = datetime.now()
        self.cursor.execute("SELECT id, link, create_at, expire_at FROM url WHERE expire_at <= ?", (current_date,))
        expired_links = self.cursor.fetchall()

        for link_data in expired_links:
            print(f"Lien expiré - ID : {link_data[0]} - Lien : {link_data[1]} - Date de création : {link_data[2]} - Date d'expiration : {link_data[3]}")
            self.cursor.execute("DELETE FROM url WHERE id = ?", (link_data[0],))

    def get_short_url(self, link_id):
        """
        Récupère le lien d'origine associé à l'ID donné et génère une URL courte.

        Paramètres:
            link_id (int): L'ID du lien.

        Retourne:
            str: L'URL courte générée.
        """
        self.cursor.execute("SELECT link FROM url WHERE id = ?", (link_id,))
        result = self.cursor.fetchone()

        if result:
            link = result[0]
            short_url = f"urlshortener.fr/{link_id}"
            print(f"URL courte pour l'ID {link_id} : {short_url} - Lien d'origine : {link}")
            return short_url

        print(f"Aucun lien trouvé pour l'ID {link_id}")
        return None

    def close_connection(self):
        """
        Valide les modifications et ferme la connexion à la base de données SQLite.
        """
        self.connection.commit()
        self.connection.close()

if __name__ == "__main__":
    url_shortener = UrlShortener()
    url_shortener.inser_new_link("https://example.com")
    url_shortener.delete_old_link()
    url_shortener.close_connection()
