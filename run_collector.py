import time
import argparse
from src.db.init_db import initialize_database
import src.collector.nasdaq_scraper as scraper

def run_collector(ticker: str, once: bool = False, interval: int = 3600):
    initialize_database()

    fetch = getattr(scraper, 'fetch_historical_data', None)
    if fetch is None:
        available = sorted(name for name in dir(scraper) if not name.startswith('_'))
        raise ImportError(f"'fetch_historical_data' not found in src.collector.nasdaq_scraper. Available: {available}")

    save_fn = getattr(scraper, 'save_to_database', None)

    while True:
        try:
            result = fetch(ticker)
            if result is not None and save_fn is not None:
                try:
                    save_fn(result)
                    print(f"Data for {ticker} fetched and saved successfully.")
                except Exception as e:
                    print(f"Fetched data but failed to save for {ticker}: {e}")
            else:
                print(f"Data for {ticker} collected (function handled saving or returned None).")
        except Exception as e:
            print(f"Error collecting data for {ticker}: {e}")
        if once:
            break
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run stock data collector")
    parser.add_argument("ticker", nargs="?", help="Stock ticker symbol (e.g. AAPL)")
    parser.add_argument("--once", action="store_true", help="Run collector once and exit")
    parser.add_argument("--interval", type=int, default=3600, help="Interval seconds between runs (default 3600)")
    args = parser.parse_args()

    if args.ticker:
        run_collector(args.ticker.strip().upper(), once=args.once, interval=args.interval)
    else:
        ticker_input = input("Enter the stock ticker symbol: ").strip().upper()
        run_collector(ticker_input, once=args.once, interval=args.interval)