import requests
from pprint import pprint


def get_all_info_on_stocks() -> list:
    """Функция отправляет get запрос к API ММВБ и получает json содержащий актуальную цену по всем акциям
    торгующимся на ММВБ. После завершения торговой сессии информация актуальна на момент закрытия торгов.
    Функция возвращает список словарей с информацией по акциямю"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.moex.com',
        'Referer': 'https://www.moex.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'iss.meta': 'off',
        'iss.json': 'extended',
        'lang': 'ru',
        'security_collection': '3',
        'sort_column': 'VALTODAY',
        'sort_order': 'desc',
    }

    response = requests.get(
        'https://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities.json',
        params=params,
        headers=headers)
    return response.json()[1]['securities']


def pars_stocks_info(buy_limit: int, data: list) -> list:
    """Функция принимает на вход список с информацией по всем акциям и сумму на которую необходимо приобрести акции.
     Функция возвращает список словарей, в каждом словаре содержится наименованием акции и ценой лота при условии,
     что цена лота меньше суммы выделенной на покупку"""
    result = []
    for stock in data:
        price = float(stock.get('PREVPRICE'))
        size_lot = int(stock.get('LOTSIZE'))
        lot_price = size_lot * price
        lot_amount = buy_limit // lot_price
        if lot_price <= buy_limit:
            name = stock.get('SHORTNAME')
            result.append({
                    'title': name,
                    'lot_price': round(lot_price, 1),
                    'lot_amount': lot_amount
                })
    return result


if __name__ == '__main__':
    limit = int(input('Введите сумму, с точностью до рубля_'))
    all_stock = get_all_info_on_stocks()
    # print(all_stock)
    pprint(sorted(pars_stocks_info(limit, all_stock), key=lambda x: x['lot_price']))

