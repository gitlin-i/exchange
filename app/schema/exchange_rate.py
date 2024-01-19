
from decimal import Decimal
from pydantic import BaseModel,ConfigDict

class ExchangeRateBase(BaseModel):
    model_config = ConfigDict(
        from_attributes = True,
        frozen = False,
    )
    currency: str


class ExchangeRate(ExchangeRateBase):
    base_rate : Decimal


