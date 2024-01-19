from pytest import fixture, mark
from service.exchange_service import ExchangeService
from repository.exchange_rate_repository import ExchangeRateRepository
from service.exchange_service import ExchangeService
from schema.exchange_rate import ExchangeRate
from .setting import scope
from contextlib import asynccontextmanager
pytest_plugins = ('pytest_asyncio',)

mocking_data = [
    ExchangeRate(currency="TEST1",base_rate=0.1),
    ExchangeRate(currency="TEST2",base_rate="0.2")
]

@asynccontextmanager
async def setting_mocking_data():
    try:
        create_result = await ExchangeRateRepository.create_bulk(mocking_data)
        assert create_result == True
        yield mocking_data
    finally:
        delete_result = await ExchangeRateRepository.delete_bulk([exchange_rate.currency for exchange_rate in mocking_data])
        assert delete_result == True

@mark.asyncio(scope= scope)
async def test_exchange_rate_service_current_rate():

    async with setting_mocking_data() as data:
        read_result = await ExchangeService.current_rate_list([ex.currency for ex in mocking_data])
        assert read_result[0] == data
        assert 1== 0


    # async for mocking_data_list in setting_mocking_data:
    #     for mocking_data in mocking_data_list:
    #         exchange_rate = await ExchangeService.current_rate(mocking_data.currency)
    #         assert exchange_rate == mocking_data
    #         assert 1== 0



# @mark.asyncio(scope= scope)
# async def test_exchange_rate_service_current_rate_list(setting_mocking_data):
#     async for mocking_data_list in setting_mocking_data:
#         exchange_rate_list = await ExchangeService.current_rate_list([mocking_data.currency for mocking_data in mocking_data_list])
#         assert exchange_rate_list == mocking_data_list


# @fixture
# def exchange_rate_all() :
#     read_result = ExchangeService.current_rate_all()
#     yield read_result

# @mark.parametrize("currency",[
#     ("USD"),("KRW")
# ])
# def test_exchange_rate_current_rate(currency, exchange_rate_all: list):
#     result = ExchangeService.current_rate( currency)

#     find_one = [exchange_rate.base_rate for exchange_rate in exchange_rate_all if exchange_rate.currency == currency]
#     target_exchange_rate = ExchangeRate(**{   
#         "currency": currency,
#         "base_rate": find_one[0]
#     })
#     assert result == target_exchange_rate
    

# @mark.parametrize("currency_codes",[
#     (["USD","JPY(100)","Q1W","NZD"]),
#     (["1234567891011"])
# ])
# def test_exchange_rate_current_rate_list(currency_codes, exchange_rate_all: list[ExchangeRate]):
#     read_result = ExchangeService.current_rate_list(currency_codes)

#     def mapping(currency_code) -> ExchangeRate | None:
#         find_one = [ exchange_rate for exchange_rate in exchange_rate_all if exchange_rate.currency == currency_code]
#         if not find_one:
#             return None
#         return ExchangeRate(currency=currency_code,base_rate= find_one[0].base_rate)
    
#     expected_result = [mapping(currency_code) for currency_code in currency_codes]
#     fail_input = [ currency_codes[i] for i, result in enumerate( expected_result) if result is None]
#     expected_result.remove(None)
#     expected_result.sort(key= lambda x: x.currency)

    
#     assert read_result == (expected_result, fail_input)