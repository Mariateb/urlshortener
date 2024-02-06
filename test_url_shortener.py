# Save this as test_url_shortener.py
from url_shortener_class import UrlShortener

def test_url_shortener():
    url_shortener = UrlShortener("test_database.db")

    # Insert a new link
    link_id = url_shortener.inser_new_link("https://example.com", days=10)

    # Generate the short URL from the ID
    short_url = url_shortener.get_short_url(link_id="lol")
    print(f"{short_url}")

    # Check and delete expired links
    url_shortener.delete_old_link()

    # Close the connection
    url_shortener.close_connection()

if __name__ == "__main__":
    test_url_shortener()
