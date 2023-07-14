from pprint import pprint
import requests
import json

from stocks_lotsize import get_all_stocks_lot_size


def get_action_data():
    """Функция отправляет get запрос к api компании БКС и получает json содержащий актуальную цену по всем акциям
    торгующимся на ММВБ. Информация во время проведения торговой сессии поступает с 15-и минутной задержкой,
     в связи с тем что используется бесплатный api. После завершения торговой сессии информация актуальна на момент
     закрытия торгов. Функция возвращает json-объект."""
    url: str = 'https://api.bcs.ru/partner/quotations?portfolio_ids%5B0%5D=113&portfolio_ids%5B1%5D=114&sorting=1' \
               '&sorting_order=asc&limit=300 '
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                   'Safari/537.36',
               'partner-token': 'A5264D52-1510-4E42-8E90-E729FF405646',
               'Accept': '*/*'}

    result = requests.get(url=url, headers=headers).json()
    return result


def pars_json(equity_list: json, size_lot: json, buy_limit: int) -> list:
    """Функция принимает на вход список акций по которым необходимо собирать информацию. Функция открывает файл с
    актуальной информацией по всем акциям и возвращает список словарей с ценой акций на текущую дату"""
    result = []
    for equity in equity_list['data']:
        short_name = equity.get('secur_code')
        price = equity.get('last_price')
        lot_price = size_lot[short_name].get("lot_size") * float(price)
        if lot_price <= buy_limit:
            name = equity.get('issuer')
            result.append({
                    'title': name,
                    'lot_price': round(lot_price, 1)
                    })
    return result


if __name__ == '__main__':
    limit = int(input('Введите сумму, с точностью до рубля_'))
    all_stock = get_action_data()
    lot_size = get_all_stocks_lot_size()
    pprint(sorted(pars_json(all_stock, lot_size, limit), key=lambda x: x['lot_price']))
