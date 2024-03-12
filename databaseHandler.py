import sqlite3
from datetime import datetime, timedelta
from typing import Any, Tuple, List


class DatabaseHandler:

    def __init__(self, dbFilename: str = "urlshortener.db"):
        self.connection = sqlite3.connect(dbFilename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS links(
            id TEXT PRIMARY KEY,
            link TEXT,
            created_at DATETIME,
            expires_at DATETIME)
            """)
        self.connection.commit()

    def insertLink(self, link: str, hashedLink: str, duration: int = 180):
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=duration)

        self.cursor.execute("""
        INSERT INTO links VALUES (?, ?, ?, ?)""",
                            (hashedLink,
                             link,
                             created_at,
                             expires_at))
        self.connection.commit()
        return self.cursor.lastrowid

    def deleteOldLinks(self):
        current_date = datetime.now()
        self.cursor.execute("SELECT id FROM links WHERE expires_at <= ?", (current_date,))
        expired_links = self.cursor.fetchall()

        for link in expired_links:
            self.cursor.execute("DELETE FROM links WHERE id = ?", (link[0],))

    def getLink(self, hashing) -> str | None:
        self.cursor.execute("SELECT link FROM links WHERE id = ?", (hashing,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def close_connection(self):
        self.connection.close()

    def get_shortened_urls_from_database_user(self) -> Tuple[List[str], List[str]]:
        conn = sqlite3.connect('urlshortener.db')
        cursor = conn.cursor()
        user_id = '018794d4'
        cursor.execute(
            f"SELECT id, link FROM links WHERE id IN (SELECT fk_link_id FROM Utilisateur_Lien WHERE fk_user_id='{user_id}')")
        results = cursor.fetchall()
        conn.close()
        shortened_urls = [row[0] for row in results]
        origined_urls = [row[1] for row in results]
        return shortened_urls, origined_urls

    def get_shortened_urls_from_database_all(self) -> List[str]:
        conn = sqlite3.connect('urlshortener.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, link FROM links")
        results = cursor.fetchall()
        # print(results)
        conn.close()
        shortened_urls = [row[0] for row in results]
        origined_urls = [row[1] for row in results]
        return shortened_urls, origined_urls