import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
sys.path.append(str(Path(__file__).parent))
from src.collector.nasdaq_scraper import save_to_database

def generate_sample_data(ticker, days=30):
    base_price = random.uniform(100, 200)
    data = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        open_price = round(base_price + random.uniform(-5, 5), 2)
        close_price = round(open_price * random.uniform(0.98, 1.02), 2)
        high = round(max(open_price, close_price) * random.uniform(1.0, 1.03), 2)
        low = round(min(open_price, close_price) * random.uniform(0.97, 1.0), 2)
        volume = random.randint(100000, 1000000)
        
        data.append((
            ticker.upper(),
            date,
            open_price,
            high,
            low,
            close_price,
            volume
        ))
    
    return data

def main():
    print("Gerando dados de exemplo...")
    
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']
    
    for ticker in tickers:
        print(f"Gerando dados para {ticker}...")
        sample_data = generate_sample_data(ticker)
        save_to_database(sample_data)
    
    print("Dados de exemplo gerados com sucesso!")

if __name__ == "__main__":
    main()