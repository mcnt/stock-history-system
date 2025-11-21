from flask import Flask, jsonify, request, render_template
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.db.models import Base, Asset, Price, get_prices_by_ticker
from src.collector.nasdaq_scraper import fetch_historical_data, save_to_database
import os
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
database_url = "sqlite:///stock_history.db"
engine = create_engine(database_url, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

def get_db_session():
    """Cria uma nova sessão do banco de dados"""
    return Session(engine)

@app.route('/')
def index():
    """Rota principal que serve a página HTML"""
    return render_template('index.html')

@app.route('/api/prices/<ticker>', methods=['GET'])
def get_prices(ticker: str):
    """Retorna os preços históricos para um ticker específico"""
    session = get_db_session()
    try:
        prices = get_prices_by_ticker(ticker, session=session)
        if not prices:
            return jsonify({"error": f"No data found for ticker '{ticker}'"}), 404
        
        return jsonify({
            "ticker": ticker,
            "prices": prices
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/collect/<ticker>', methods=['POST'])
def collect_data(ticker: str):
    """Rota para coletar dados de um ticker específico"""
    try:
        data = fetch_historical_data(ticker)
        if not data:
            return jsonify({"error": f"No data found for ticker '{ticker}'"}), 404
        
        save_to_database(data)
        
        return jsonify({
            "message": f"Successfully collected {len(data)} records for {ticker}",
            "count": len(data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/seed', methods=['GET', 'POST'])
def seed_data():
    """Rota para popular o banco com dados de exemplo"""
    ticker = request.args.get('ticker', 'AAPL')
    session = get_db_session()
    try:
        asset = session.query(Asset).filter_by(ticker=ticker).first()
        if not asset:
            asset = Asset(ticker=ticker)
            session.add(asset)
            session.commit()
            
            prices = [
                Price(
                    asset_id=asset.id,
                    date=datetime.now().date().isoformat(),
                    open_price=150.0,
                    high_price=155.0,
                    low_price=148.0,
                    close_price=152.5,
                    volume=1000000
                )
            ]
            session.bulk_save_objects(prices)
            session.commit()
        
        return jsonify({"message": f"Sample data created for {ticker}"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)