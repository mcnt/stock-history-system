import requests
from pathlib import Path
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, Float,
                        String, Date, ForeignKey, select, delete, insert)
from datetime import datetime, timedelta
import time
import random

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "stock_history.db"

def fetch_historical_data(ticker: str, years: int = 1):
    """
    Busca dados históricos de ações diretamente do site da NASDAQ.
    Retorna lista de tuplas: (ticker, data_iso, open, high, low, close, volume)
    """
    ticker = ticker.strip().upper()
    print(f"[fetch] Buscando dados para {ticker} ({years} ano(s)) no site da NASDAQ...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nasdaq.com/'
    }
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    
    url = f"https://api.nasdaq.com/api/quote/{ticker}/historical"
    
    params = {
        'assetclass': 'stocks',
        'fromdate': start_date.strftime('%Y-%m-%d'),
        'todate': end_date.strftime('%Y-%m-%d'),
        'limit': '9999'
    }
    
    try:
        response = requests.get(
            url, 
            headers=headers, 
            params=params,
            timeout=30
        )
        
        if response.status_code != 200:
            
            return []
            
        data = response.json()
        
        if not data.get('data') or not data['data'].get('tradesTable', {}).get('rows'):
            return []
        
        rows = []
        for row in data['data']['tradesTable']['rows']:
            try:
                date_parts = row['date'].split('/')
                if len(date_parts) == 3:
                    formatted_date = f"{date_parts[2]}-{date_parts[0].zfill(2)}-{date_parts[1].zfill(2)}"
                else:
                    continue
                    
                rows.append((
                    ticker,
                    formatted_date,
                    float(row['open'].replace('$', '').replace(',', '') or 0),
                    float(row['high'].replace('$', '').replace(',', '') or 0),
                    float(row['low'].replace('$', '').replace(',', '') or 0),
                    float(row['close'].replace('$', '').replace(',', '') or 0),
                    int(row['volume'].replace(',', '') or 0)
                ))
            except (ValueError, KeyError) as e:
                continue
        
        rows.sort(key=lambda x: x[1])
        
        return rows
        
    except requests.exceptions.RequestException as e:
        return []
    except Exception as e:
        return []

def save_to_database(data):
    """
    Salva dados históricos no banco SQLite.
    Cria tabelas 'assets' e 'prices' se não existirem.
    """
    if not data:
        print("[save] Nenhum dado para salvar.")
        return

    ticker = data[0][0]

    engine = create_engine(f"sqlite:///{DB_PATH}")
    metadata = MetaData()

    assets = Table('assets', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('ticker', String, unique=True, nullable=False),
                   extend_existing=True)
    prices = Table('prices', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('asset_id', Integer, ForeignKey('assets.id'), nullable=False),
                   Column('date', Date, nullable=False),
                   Column('open_price', Float),
                   Column('high_price', Float),
                   Column('low_price', Float),
                   Column('close_price', Float),
                   Column('volume', Integer),
                   extend_existing=True)

    metadata.create_all(engine)

    with engine.begin() as conn:
        asset = conn.execute(select(assets).where(assets.c.ticker == ticker)).first()
        if not asset:
            result = conn.execute(insert(assets).values(ticker=ticker))
            asset_id = result.inserted_primary_key[0]
        else:
            asset_id = asset[0]
            conn.execute(delete(prices).where(prices.c.asset_id == asset_id))
        price_data = []
        for row in data:
            try:
                date_obj = datetime.strptime(row[1], '%Y-%m-%d').date()
                
                price_data.append({
                    'asset_id': asset_id,
                    'date': date_obj,
                    'open_price': row[2],
                    'high_price': row[3],
                    'low_price': row[4],
                    'close_price': row[5],
                    'volume': row[6]
                })
            except Exception as e:
                pass

        if price_data:
            conn.execute(insert(prices), price_data)

if __name__ == "__main__":
    ticker = "AAPL"
    data = fetch_historical_data(ticker, years=1)

    if data:
        print(f"Primeiro registro: {data[0]}")
        print(f"Último registro: {data[-1]}")
        save_to_database(data)
    else:
        print("Nenhum dado obtido.")