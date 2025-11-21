import unittest
from src.collector.nasdaq_scraper import fetch_historical_data

class TestNasdaqScraper(unittest.TestCase):

    def test_fetch_historical_data_valid_ticker(self):
        ticker = "AAPL"
        data = fetch_historical_data(ticker)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_fetch_historical_data_invalid_ticker(self):
        ticker = "INVALID"
        with self.assertRaises(ValueError):
            fetch_historical_data(ticker)

    def test_fetch_historical_data_empty_ticker(self):
        ticker = ""
        with self.assertRaises(ValueError):
            fetch_historical_data(ticker)

if __name__ == '__main__':
    unittest.main()