import os
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, func
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

Base = declarative_base()

class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)

    prices = relationship("Price", back_populates="asset")

class Price(Base):
    __tablename__ = 'prices'
    
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    date = Column(String, nullable=False) 
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

    asset = relationship("Asset", back_populates="prices")

_env_db = os.getenv("DATABASE_URL", "").strip()
if not _env_db or _env_db.lower().startswith("your_") or _env_db.lower() in ("none", "null"):
    database_url = "sqlite:///./stock_history.db"
else:
    database_url = _env_db

try:
    if database_url.startswith("sqlite"):
        engine = create_engine(database_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(database_url)
except Exception:
    database_url = "sqlite:///./stock_history.db"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_prices_by_ticker(ticker: str, session: Session = None):
    """
    Retorna uma lista de dicionários com os dados de preços para o ticker informado.
    Se nenhuma sessão for fornecida, a função cria e encerra uma automaticamente.
    A consulta não diferencia maiúsculas de minúsculas e os preços são retornados em ordem de data.
    """
    if not ticker:
        return None

    ticker = ticker.strip()
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True

    try:
        asset = session.query(Asset).filter(func.lower(Asset.ticker) == ticker.lower()).first()
        if not asset:
            return None
        price_rows = session.query(Price).filter(Price.asset_id == asset.id).order_by(Price.date).all()

        prices = [
            {
                "date": p.date,
                "open": p.open_price,
                "high": p.high_price,
                "low": p.low_price,
                "close": p.close_price,
                "volume": p.volume,
            }
            for p in price_rows
        ]
        return prices
    finally:
        if close_session:
            session.close()

def seed_sample_data(ticker: str = "AAPL"):
    """
    Cria um ativo simples e algumas linhas de preços para teste local.
    Retorna os preços do ativo criado/actualizado como dicionários.
    """
    ticker = (ticker or "").strip().upper()
    session = SessionLocal()
    try:
        asset = session.query(Asset).filter(func.lower(Asset.ticker) == ticker.lower()).first()
        if not asset:
            asset = Asset(ticker=ticker)
            session.add(asset)
            session.commit()

        existing = session.query(Price).filter(Price.asset_id == asset.id).first()
        if not existing:
            sample_prices = [
                Price(asset_id=asset.id, date="2025-11-18", open_price=150.0, high_price=152.0, low_price=149.0, close_price=151.0, volume=100000),
                Price(asset_id=asset.id, date="2025-11-19", open_price=151.0, high_price=153.0, low_price=150.0, close_price=152.0, volume=110000),
                Price(asset_id=asset.id, date="2025-11-20", open_price=152.0, high_price=154.0, low_price=151.0, close_price=153.0, volume=120000),
            ]
            session.add_all(sample_prices)
            session.commit()

        return get_prices_by_ticker(ticker, session=session)
    finally:
        session.close()