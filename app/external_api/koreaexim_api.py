import requests
from secret.appkey import KOREAEXIM
from exception.exception import EmptyListError
base_url = "https://www.koreaexim.go.kr/site/program/financial"

authkey = KOREAEXIM["authkey"]


def get_exchange_rate(search_date = None):
    
    url = "/exchangeJSON"
    data_type = "AP01" #환율
    params = {
        "authkey" : authkey,
        "searchdate": search_date, #default now
        "data" : data_type
    }
    response = requests.get(base_url + url, params=params)
    #공휴일 조회시 []반환

    result = response.json()

    if not result:
        raise EmptyListError
    return result