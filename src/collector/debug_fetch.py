import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from src.collector import nasdaq_scraper as scraper

ticker = "AAPL"
print("Has fetch_historical_data:", hasattr(scraper, "fetch_historical_data"))
print("Has save_to_database:", hasattr(scraper, "save_to_database"))

try:
    result = scraper.fetch_historical_data(ticker)
    print("fetch_historical_data returned type:", type(result))
    if isinstance(result, (list, tuple)):
        print("first items:", result[:3])
    else:
        print("result repr:", repr(result)[:1000])
except Exception as e:
    print("Error calling fetch_historical_data:", e)

if hasattr(scraper, "save_to_database") and result:
    try:
        scraper.save_to_database(result)
        print("save_to_database executed successfully")
    except Exception as e:
        print("save_to_database error:", e)