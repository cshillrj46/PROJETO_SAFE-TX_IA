# File: backend/database.py

from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./safetx.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class TransactionRecord(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    recipient = Column(String, index=True)
    amount_eth = Column(Float)
    risk = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ReclassificationLog(Base):
    __tablename__ = "reclassifications"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, index=True)
    old_risk = Column(String)
    new_risk = Column(String)
    reason = Column(String)
    reclassified_by = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
