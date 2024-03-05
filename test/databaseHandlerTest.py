import os.path
import sqlite3
import unittest
from datetime import date, timedelta

from databaseHandler import DatabaseHandler


class DatabaseHandlerTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.exists('test.db'):
            clearTestDatabase()
        self.databaseHandler = DatabaseHandler('test.db')

    def test(self):
        index = self.databaseHandler.insertLink('http://test.com', 'test')
        self.assertEqual('test', index)

        link = self.databaseHandler.getLink('test')
        self.assertEqual('http://test.com', link)

        yesterday = date.today() - timedelta(days=1)
        self.databaseHandler.cursor.execute('UPDATE links SET expires_at = ? WHERE id = ?',
                                            (yesterday, 'test'))

        self.databaseHandler.deleteOldLinks()
        self.assertIsNone(self.databaseHandler.getLink('test'))


def clearTestDatabase():
    db = sqlite3.connect('test.db')

    db.execute("DROP TABLE IF EXISTS links")
    db.commit()

    db.close()


if __name__ == '__main__':
    unittest.main()
