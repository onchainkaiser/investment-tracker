from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid
from datetime import datetime

class Investment:
    def __init__(self, asset_name, amount_invested, current_value, chain_name, currency):
        self.id = str(uuid.uuid4())
        self.asset_name = asset_name
        self.amount_invested = amount_invested
        self.current_value = current_value
        self.chain_name = chain_name
        self.currency = currency
        self.date_invested = datetime.now()

from sqlalchemy import Column, String, Float, DateTime, func
from database import Base
import uuid

class Investment(Base):
    __tablename__ = "investments"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    asset_name = Column(String, nullable=False)
    amount_invested = Column(Float, nullable=False)   # 👈 use Float not float
    current_value = Column(Float, nullable=False)     # 👈 same here
    chain_name = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    date_invested = Column(DateTime(timezone=True), server_default=func.now())
