from datetime import datetime, timedelta
from exception.exception import EmptyListError
from schema.exchange_rate import ExchangeRate
from repository.exchange_rate_repository import ExchangeRateRepository
from external_api.koreaexim_api import get_exchange_rate
from pydantic import validate_call


def replace(target):
    #데이터 정제 로직
    ##deal_bas_r 은 매매기준율
    target['deal_bas_r'] = target['deal_bas_r'].replace(",","")
    return target

class ExchangeService:

    @classmethod
    @validate_call
    async def current_rate(cls, currency_code : str) -> ExchangeRate:
        read_result = await ExchangeRateRepository.read(currency_code= currency_code)
        exchange_rate = ExchangeRate(**read_result[0].__dict__)
        return exchange_rate
        
    @classmethod
    @validate_call
    async def current_rate_list(cls,currency_codes : list[str]) -> tuple[list[ExchangeRate] , list[str]] :
        read_result = await ExchangeRateRepository.read_bulk(currency_codes)
        exchange_rate_list = [ExchangeRate(**exchange_rate[0].__dict__) for exchange_rate in read_result]
        read_currency_codes = [ exchange_rate.currency for exchange_rate in exchange_rate_list]
        not_read_input = [currency_code for currency_code in currency_codes if currency_code not in read_currency_codes]
        return (exchange_rate_list, not_read_input)
        

    @classmethod
    async def init_exchange_rate(cls) -> bool:
        exchange_rate_in_db = await ExchangeRateRepository.read("KRW")
        if not exchange_rate_in_db:
            
            try:
                exchange_rate_list = get_exchange_rate()
            except EmptyListError:
                #최신 환율 조회(10일 이내)
                today = datetime.now().date()
                for i in range(1,11):
                    td = timedelta(days=i)
                    exchange_rate_list = get_exchange_rate(search_date= str(today - td))
                    if exchange_rate_list:
                        break
            exchange_rate_list = [replace(target=exchange_rate) for exchange_rate in exchange_rate_list]
            exchange_rates = [ExchangeRate(currency= exchange_rate["cur_unit"] , base_rate= exchange_rate["deal_bas_r"]) for exchange_rate in exchange_rate_list]
            create_result = ExchangeRateRepository.create_bulk(exchange_rates)
            return create_result
                
    @classmethod
    def update_exchange_rate(cls) -> bool:
        
        exchange_rate_list = get_exchange_rate()
        exchange_rate_list = [replace(target=exchange_rate) for exchange_rate in exchange_rate_list]
        exchange_rates = [ExchangeRate(currency= exchange_rate["cur_unit"] , base_rate= exchange_rate["deal_bas_r"]) for exchange_rate in exchange_rate_list]
        update_result = ExchangeRateRepository.update_bulk(exchange_rates)
        return update_result