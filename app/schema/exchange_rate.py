
from decimal import Decimal
from typing import List
from pydantic import BaseModel

class ExchangeRateBase(BaseModel):

    currency: str
    class Config:
        orm_mode = True
        allow_mutation :False


class ExchangeRate(ExchangeRateBase):
    base_rate : Decimal


