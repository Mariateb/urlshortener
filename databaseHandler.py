import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Any
from fastapi import HTTPException

class DatabaseHandler:

    def __init__(self, dbFilename: str = "urlshortener.db"):
        self.dbFilename = dbFilename
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

    def insertLink(self, link: str, hashedLink: str, duration: int = 180) -> str | None:
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=duration)

        try:
            self.cursor.execute("SELECT id FROM links WHERE id = ?", (hashedLink,))
        except sqlite3.OperationalError:
            self.resetConnection()
            return
        links = self.cursor.fetchall()

        if len(links) == 0:
            return hashedLink

        self.cursor.execute("""
        INSERT INTO links VALUES (?, ?, ?, ?)""",
                            (hashedLink,
                             link,
                             created_at,
                             expires_at))
        try:
            self.connection.commit()
        except sqlite3.OperationalError as e:
            self.resetConnection()
            logging.error(e)
            raise HTTPException(status_code=500, detail="Failed to insert link")
        return hashedLink

    def deleteOldLinks(self) -> None:
        current_date = datetime.now()
        try:
            self.cursor.execute("SELECT id FROM links WHERE expires_at <= ?", (current_date,))
        except sqlite3.OperationalError as e:
            self.resetConnection()
            logging.error(e)
            return
        expired_links = self.cursor.fetchall()

        for link in expired_links:
            self.cursor.execute("DELETE FROM links WHERE id = ?", (link[0],))
        self.connection.commit()

    def getLink(self, hashing) -> str | None:
        self.cursor.execute("SELECT link FROM links WHERE id = ?", (hashing,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def resetConnection(self):
        self.connection.close()
        self.connection = sqlite3.connect(self.dbFilename)
        self.cursor = self.connection.cursor()
