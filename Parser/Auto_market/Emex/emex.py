import requests
from pprint import pprint

from pars_emex import get_analog_or_replacement_parts, get_original_parts

part_number = input('Введите номер детали для поиска по базе_:')
base_search_url = 'https://emex.ru/api/search/search2'
alter_search_url = 'https://emex.ru/api/search/search'

headers_search = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Access-Control-Allow-Origin': 'https://emex.ru',
    'Referer': 'https://emex.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'cache-control': 'no-cache',
    'expires': '0',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
}

params_search = {
    'isHeaderSearch': 'false',
    'showAll': 'true',
    'searchString': part_number,
    'locationId': 23438
}

alter_params_search = {
    'detailNum': '',
    'make': '',
    'locationId': '23438',
    'showAll': 'true'
}


def get_search_result(address: str, headers: dict, params: dict) -> dict:
    """Функция для отправки запроса к API.
    На вход функции подается url-адрес, хэдер и параметры для запроса. Функция возвращает словарь с результатами
    поиска для дальнейшей обработки"""
    ses = requests.Session()
    search_result = ses.get(url=address,
                            params=params, headers=headers).json()
    return search_result['searchResult']


result = get_search_result(base_search_url, headers_search, params_search)

match result:
    case {'noResults': True}:
        print('По данному номеру детали нет предложений')
    case {'originals': original, 'analogs': analog, 'replacements': replacement}:
        pprint(get_original_parts(original))
        pprint(get_analog_or_replacement_parts(replacement))
        pprint(get_analog_or_replacement_parts(analog))
    case {'originals': original, 'analogs': analog}:
        pprint(get_original_parts(original))
        pprint(get_analog_or_replacement_parts(analog))
    case _:
        part_vars: list = [{'make': i['make'], 'number': i['num']} for i in result['makes']['list']]
        alter_params_search['make'], alter_params_search['detailNum'] = part_vars[0].values()
        alter_result: object = requests.get(url=alter_search_url, headers=headers_search,
                                            params=alter_params_search).json()
        match alter_result['searchResult']:
            case {'originals': original, 'analogs': analog, 'replacements': replacement}:
                pprint(get_original_parts(original))
                pprint(get_analog_or_replacement_parts(replacement))
                pprint(get_analog_or_replacement_parts(analog))
            case {'originals': original, 'analogs': analog}:
                pprint(get_original_parts(original))
                pprint(get_analog_or_replacement_parts(analog))
