# Sauvegardez ceci en tant que test_url_shortener.py
from databaseHandler import UrlShortener

def test_url_shortener():
    """
    Un script de test pour la classe UrlShortener, démontrant l'insertion d'un nouveau lien,
    la génération d'une URL courte, la suppression des liens expirés et la fermeture de la connexion.
    """

    # Création d'une instance de la classe UrlShortener avec une base de données de test
    url_shortener = UrlShortener("test_database.db")

    # Insertion d'un nouveau lien avec une durée de validité de 10 jours
    link_id = url_shortener.inser_new_link("https://example.com", days=10)

    # Génération de l'URL courte à partir de l'ID
    short_url = url_shortener.get_short_url(link_id)

    # Affichage de l'URL courte
    print(f"URL courte générée : {short_url}")

    # Vérification et suppression des liens expirés
    url_shortener.delete_old_link()

    # Fermeture de la connexion à la base de données
    url_shortener.close_connection()

if __name__ == "__main__":
    # Appel de la fonction de test
    test_url_shortener()
