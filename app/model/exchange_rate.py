
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  TIMESTAMP, String, text
from sqlalchemy.dialects.mysql import DECIMAL
from datetime import datetime
from database import Base
class ExchangeRateModel(Base):
    __tablename__ = "exchange_rate"
    currency : Mapped[str] = mapped_column(String(8),primary_key=True)
    base_rate : Mapped[DECIMAL] = mapped_column(DECIMAL(precision=9,scale=2))
    updated_date : Mapped[datetime] = mapped_column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))