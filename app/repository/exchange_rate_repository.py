from sqlalchemy import Row, delete, insert,select, update

from pydantic import validate_call
from model.exchange_rate import ExchangeRateModel
from schema.exchange_rate import ExchangeRate
from database import AsyncSessionLocal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError,UnmappedInstanceError


class ExchangeRateRepository:



    @classmethod
    @validate_call
    async def read(cls, currency_code: str) ->Row[ExchangeRateModel] | None:
        async with AsyncSessionLocal() as session:
            stmt = select(ExchangeRateModel).where(ExchangeRateModel.currency == currency_code)
            result = await session.execute(stmt)
            return result.one()
    
    @classmethod
    @validate_call
    async def read_bulk(cls,currency_codes: list[str]) -> list[Row[ExchangeRateModel]] | None:
        async with AsyncSessionLocal() as session:
            stmt = select(ExchangeRateModel).where(ExchangeRateModel.currency.in_(currency_codes))
            result = await session.execute(stmt)
            return list(result.all())
        
    @classmethod
    @validate_call
    async def create(cls, exchange_rate : ExchangeRate) -> bool:
        result = False
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin(): 
                    mapped_model = ExchangeRateModel(**exchange_rate.model_dump())
                    session.add(mapped_model)
        except AttributeError as e:
            print("속성 에러, 매개변수 타입 확인 : ", e)
        except IntegrityError as e:
            print("중복 키, 이미 키가 존재함.",e)
        else:
            result = True
        return result
    @classmethod
    async def create_bulk(cls,exchange_rate_list: list[ExchangeRate]) -> bool:
        result = False
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin(): 
                    stmt = insert(ExchangeRateModel)
                    await session.execute(stmt,exchange_rate_list)

        except AttributeError as e:
            print("속성 에러, 매개변수 타입 확인 : ", e)
        except IntegrityError as e:
            print("중복 키, 이미 키가 존재함.",e)
        else:
            result = True
        return result

    @classmethod
    @validate_call
    async def delete(cls, currency:str ) -> bool: 
        result = False
        try: 
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    target = await session.get(ExchangeRateModel,currency)
                    
                    if target:
                        await session.delete(target)
        except UnmappedInstanceError as e:
            print("존재하지 않는 인스턴스: ", e)
        else:
            result = True
        return result

    @classmethod
    @validate_call
    async def delete_bulk(cls, currency_list:list[str] ) -> bool: 
        result = False
        try: 
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    stmt = delete(ExchangeRateModel).where(ExchangeRateModel.currency.in_(currency_list))
                    await session.execute(stmt)
        except UnmappedInstanceError as e:
            print("존재하지 않는 인스턴스: ", e)
        else:
            result = True
        return result
    

        

    @classmethod
    @validate_call
    async def update(cls, exchange_rate: ExchangeRate) -> bool:
        result = False
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    stmt = update(ExchangeRateModel)
                    result = await session.execute(stmt,[exchange_rate.model_dump()])    
        except StaleDataError as e:
            print("0 matched...",e)
            raise e
        else:
            result = True
        return result
    
    @classmethod
    @validate_call
    async def update_bulk(cls, exchange_rates: list[ExchangeRate]) -> bool:
        result = False
        try:
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    stmt = update(ExchangeRateModel)
                    mapped_list = [ exchange_rate.model_dump() for exchange_rate in exchange_rates ]
                    result = await session.execute(stmt,mapped_list)    
        except StaleDataError as e:
            print("0 matched...",e)
            raise e
        else:
            result = True
        return result




