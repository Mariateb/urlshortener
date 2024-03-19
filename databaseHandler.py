import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Tuple, List

from typing import Any
from fastapi import HTTPException

import api


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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
            login TEXT PRIMARY KEY,
            password TEXT)
            """)
        self.cursor.execute("""
            create table IF NOT EXISTS usersLink(
                login_users text
                    constraint usersLink_users_login_fk
                        references users,
                id_link     text
                    constraint usersLink_links_id_fk
                        references links
            )""")

        self.connection.commit()

    def insert_link(self, link: str, hashedLink: str, userId, duration: int = 180) -> str | None:

        if duration <= 0:
            raise HTTPException(status_code=500, detail="Failed to insert link : Invalid duration")

        created_at = datetime.now()
        expires_at = created_at + timedelta(days=duration)

        try:
            self.cursor.execute("SELECT id FROM links WHERE id = ?", (hashedLink,))
        except sqlite3.OperationalError:
            self.resetConnection()
            return
        links = self.cursor.fetchall()

        if len(links) > 0:
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

        if userId != None :
            self.cursor.execute("""
                    INSERT INTO usersLink VALUES (?, ?)""",
                                (userId,
                                 hashedLink))
            try:
                self.connection.commit()
            except sqlite3.OperationalError as e:
                self.resetConnection()
                logging.error(e)
                raise HTTPException(status_code=500, detail="Failed to insert link")

        return hashedLink

    def delete_old_links(self) -> None:
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

    def get_link(self, hashing) -> str | None:
        self.cursor.execute("SELECT link FROM links WHERE id = ?", (hashing,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def resetConnection(self):
        self.connection.close()
        self.connection = sqlite3.connect(self.dbFilename)
        self.cursor = self.connection.cursor()

    def create_user(self, login, password):
        try:
            self.cursor.execute("""
            INSERT INTO users VALUES (?, ?)""",
                            (login,
                             password))
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return None
        self.connection.commit()
        return self.cursor.lastrowid

    def get_user(self, login, password):
        self.cursor.execute("SELECT login FROM users WHERE login = ? AND password = ?", (login,password,))
        return self.cursor.fetchone()


    def get_shortened_urls_from_database_user(self,cookie) -> Tuple[List[str], List[str]]:
        conn = sqlite3.connect('urlshortener.db')
        cursor = conn.cursor()
        user_id = cookie
        cursor.execute(
            "SELECT id, link FROM links WHERE id IN ( SELECT id_link FROM usersLink WHERE login_users = ? )",(user_id,)
        )
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