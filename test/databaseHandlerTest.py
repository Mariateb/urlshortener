import os.path
import sqlite3
import unittest
from datetime import timedelta, datetime

from databaseHandler import DatabaseHandler


class DatabaseHandlerTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.exists('test.db'):
            clearTestDatabase()
        self.databaseHandler = DatabaseHandler('test.db')

    def test(self):
        index = self.databaseHandler.insert_link('http://test.com', 'test', 20)
        self.assertEqual('test', index)

        link = self.databaseHandler.get_link('test')
        self.assertEqual('http://test.com', link)

        self.databaseHandler.cursor.execute('SELECT * FROM links WHERE id = ?', ('test',))
        res = list(self.databaseHandler.cursor.fetchall())

        creationDate = datetime.strptime(res[0][2], '%Y-%m-%d %H:%M:%S.%f')
        expirationDate = datetime.strptime(res[0][3], '%Y-%m-%d %H:%M:%S.%f')

        self.assertEqual(creationDate + timedelta(days=20), expirationDate)

        expectedVisits = 0
        visits = self.databaseHandler.getVisits('test')
        self.assertEqual(visits, expectedVisits)

        yesterday = datetime.today() - timedelta(days=1)
        self.databaseHandler.cursor.execute('UPDATE links SET expires_at = ? WHERE id = ?',
                                            (yesterday, 'test'))
        self.databaseHandler.connection.commit()

        self.databaseHandler.addVisitor('test')

        expectedVisits = 1
        visits = self.databaseHandler.getVisits('test')

        self.assertEqual(visits, expectedVisits)


        self.databaseHandler.delete_old_links()
        self.assertIsNone(self.databaseHandler.get_link('test'))

        self.assertEqual(True, self.databaseHandler.delete_link("urlImpossible"))

def clearTestDatabase():
    db = sqlite3.connect('test.db')

    db.execute("DROP TABLE IF EXISTS links")
    db.commit()

    db.close()


if __name__ == '__main__':
    unittest.main()
