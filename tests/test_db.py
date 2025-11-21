import unittest
import sqlite3
from src.db.init_db import initialize_db

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect(':memory:')  # Use in-memory database for testing
        cls.cursor = cls.connection.cursor()
        initialize_db(cls.cursor)  # Initialize the database schema

    def test_insert_asset(self):
        self.cursor.execute("INSERT INTO assets (symbol) VALUES ('AAPL')")
        self.connection.commit()
        
        self.cursor.execute("SELECT * FROM assets WHERE symbol='AAPL'")
        asset = self.cursor.fetchone()
        self.assertIsNotNone(asset)
        self.assertEqual(asset[1], 'AAPL')

    def test_insert_price(self):
        self.cursor.execute("INSERT INTO assets (symbol) VALUES ('AAPL')")
        self.connection.commit()
        
        self.cursor.execute("INSERT INTO prices (asset_id, date, open, high, low, close, volume) VALUES (1, '2023-01-01', 150.00, 155.00, 149.00, 154.00, 1000000)")
        self.connection.commit()
        
        self.cursor.execute("SELECT * FROM prices WHERE asset_id=1")
        price = self.cursor.fetchone()
        self.assertIsNotNone(price)
        self.assertEqual(price[2], 150.00)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

if __name__ == '__main__':
    unittest.main()