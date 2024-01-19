
from repository.exchange_rate_repository import ExchangeRateRepository
from schema.exchange_rate import ExchangeRate
from pytest import fixture,mark
from .setting import scope

pytest_plugins = ('pytest_asyncio',)


@fixture
async def exchange_rate_repo_test_row():
    test_data = ExchangeRate(currency="TEST",base_rate="1.0")
    create_result = await ExchangeRateRepository.create(test_data)
    assert create_result == True
    yield test_data
    delete_result = await ExchangeRateRepository.delete(test_data.currency)
    assert delete_result == True
@fixture
async def exchange_rate_repo_test_row_multi():
    test_data1 = ExchangeRate(currency="TEST1",base_rate="1.0")
    test_data2 = ExchangeRate(currency="TEST2",base_rate="1.1")
    test_data3 = ExchangeRate(currency="TEST3",base_rate="1.2")
    test_data4 = ExchangeRate(currency="TEST4",base_rate="1.3")

    test_list = [test_data1,test_data2,test_data3,test_data4]
    create_result = await ExchangeRateRepository.create_bulk(test_list)
    assert create_result == True
    yield test_list
    test_str_list = [exchange_rate.currency for exchange_rate in test_list]
    delete_result = await ExchangeRateRepository.delete_bulk(test_str_list)
    assert delete_result == True

@fixture
async def exchange_rate_repo_update_test_row(exchange_rate_repo_test_row):
    async for ex in exchange_rate_repo_test_row:
        
        data_for_update = ExchangeRate(currency=ex.currency ,base_rate="1.1")
        update_result = await ExchangeRateRepository.update(data_for_update)
        assert update_result == True
        yield data_for_update

@fixture
async def exchange_rate_repo_update_test_row_multi(exchange_rate_repo_test_row_multi):
    test_data1 = ExchangeRate(currency="TEST1",base_rate="2.0")
    test_data2 = ExchangeRate(currency="TEST2",base_rate="2.1")
    test_data3 = ExchangeRate(currency="TEST3",base_rate="2.2")
    test_data4 = ExchangeRate(currency="TEST4",base_rate="2.3")
    update_test_list = [test_data1,test_data2,test_data3,test_data4]

    async for ex_list in exchange_rate_repo_test_row_multi:
        update_result = await ExchangeRateRepository.update_bulk(update_test_list)
        assert update_result == True
        yield update_test_list
    
@mark.asyncio(scope= scope)
async def test_exchange_rate_repo_read(exchange_rate_repo_test_row):

    async for ex in exchange_rate_repo_test_row:
        read_result = await ExchangeRateRepository.read("TEST")
        mapped_read_result = ExchangeRate(**read_result[0].__dict__)
        assert mapped_read_result == ex

@mark.asyncio(scope= scope)
async def test_exchange_rate_repo_read_bulk(exchange_rate_repo_test_row_multi):

    async for ex_list in exchange_rate_repo_test_row_multi:
        curreny_codes = [exchange_rate.currency for exchange_rate in ex_list]
        read_result_list = await ExchangeRateRepository.read_bulk(currency_codes=curreny_codes)
        mapped_read_result = [ ExchangeRate(**read_result[0].__dict__) for read_result in read_result_list]
        assert mapped_read_result == ex_list

@mark.asyncio(scope= scope)
async def test_exchange_rate_repo_update_read(exchange_rate_repo_update_test_row):
    async for ex in exchange_rate_repo_update_test_row:
        read_result = await ExchangeRateRepository.read("TEST")
        mapped_read_result = ExchangeRate(**read_result[0].__dict__)
        assert mapped_read_result == ex

@mark.asyncio(scope= scope)
async def test_exchange_rate_repo_update_read_bulk(exchange_rate_repo_update_test_row_multi : list[ExchangeRate]):

    async for ex_list in exchange_rate_repo_update_test_row_multi:
        currency_codes = [ex.currency for ex in ex_list]
        read_result_list = await ExchangeRateRepository.read_bulk(currency_codes)
        print(read_result_list)
        mapped_read_result = [ ExchangeRate(**read_result[0].__dict__) for read_result in read_result_list]
        assert mapped_read_result == ex_list