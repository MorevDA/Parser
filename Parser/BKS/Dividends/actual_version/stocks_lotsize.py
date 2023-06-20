import requests
import json


def get_all_stocks_lot_size():
    """ Функция для получения данных о размере лота российских ценных бумаг торгующихся на ММВБ. Функция отправляет
    запрос к api ММВБ для получения данных по размеру лота всех акций торгущихся на ММВБ. Функция возвращает
    словарь с данными по размеру лота акций"""
    result = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.moex.com',
        'Referer': 'https://www.moex.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    for start_value in range(0, 300, 100):
        params = {'_': '1687021339014', 'lang': 'ru', 'iss.meta': 'off', 'sort_order': 'asc',
                  'sort_column': 'SECID', 'start': f'{str(start_value)}', 'limit': '100',
                  'sec_type': 'stock_common_share,stock_preferred_share,stock_russian_depositary_receipt',
                  'faceunit': 'rub', 'bg': 'stock_tplus', }

        response = requests.get(
            'https://iss.moex.com/iss/apps/infogrid/stock/rates.json', params=params, headers=headers,)

        for i in response.json()['rates']['data']:
            result[i[0]] = {'name': i[1], 'ISIN': i[4], 'lotsize': int(i[29])}
    return result


def get_json_file(res):
    with open('lot_size.json', 'w', encoding='utf-8') as file:
        json.dump(res, file, ensure_ascii=False, indent=4)


def main():
    get_json_file(get_all_stocks_lot_size())


if __name__ == "__main__":
    main()
