from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import MetaData
from sqlalchemy import Column, Integer, String, Float, DateTime, func, BigInteger

models_metadata = MetaData()
Base = declarative_base(metadata=models_metadata)

class TronWallet(Base):
    __tablename__ = "tron_wallet_queries"
    metadata = models_metadata

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String(256), nullable=False)
    bandwidth = Column(BigInteger, nullable=False)
    energy = Column(BigInteger, nullable=False)
    balance_trx = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())
