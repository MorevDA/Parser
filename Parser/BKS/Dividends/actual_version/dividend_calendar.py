import requests
import json
from stocks_lotsize import get_all_stocks_lot_size


def read_json(file_name):
    """Функция для чтения json файла. На вход функции подается имя файла. Функция возвращает считанный json
    объект"""
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json(obj_mame, file_name):
    """Функция для создания json файла. На вход функции подаются объект который необходимо записать в json файл
    и имя файла в который нужно сохранить данные, имя файла указывается без расширения файла. После создания файла
    на печать выводится сообщение о создании файла"""
    with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(obj_mame, file, indent=4, ensure_ascii=False)
    print(f"json file {file_name} create")


def get_calendar_json():
    """Функция  отправляет запрос к api компании БКС для получения данных о дивидентных выплатах.
     На выходе функции, с помощью функции write_json, формирируется json файл с актуальными данными по дивидендным
     выплатам(как данные о будующих дивидендах, так и ретроспектива по  выплатам прошлых лет).
     На выходе функции возвращается json объект для дальнейшего анализа"""
    url = 'https://api.bcs.ru/divcalendar/v1/dividends?actual=1'
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                   'Safari/537.36',
               'Accept': '*/*'}
    response = requests.get(url=url, headers=headers).json()
    write_json(response, 'div_calculate')
    return response


def get_list_this_year():
    """Функция возвращает  словарь с информацией по названию компании и дивидендному периоду, размеру дивидендов на
    одну акцию, процент дивидендной доходности, дате закрытия реестра, дате последнего дня покупки акций для получения
     дивидендов, ориетировочной цене одного лота акций. Цена одного лота является ориентировочной, так как базируется на
     информации о цене акций на закрытии предыдущей торговой сессии."""
    stocks_with_div = {}
    total_list = get_calendar_json()
    lots_size = get_all_stocks_lot_size()
    for stock in total_list.get('data'):
        dividend_percent = stock.get('yield')
        company_name = stock.get('company_name')
        dividend_value = stock.get('dividend_value')
        last_buy_day = str(stock.get('last_buy_day')).split('T')[0]
        closing_date = str(stock.get('closing_date')).split('T')[0]
        price_one_stock = stock.get('close_price')
        secure_code = stock.get('secure_code')
        lot_price = lots_size[secure_code]['lotsize'] * float(price_one_stock)
        stocks_with_div[company_name] = {'dividend_value': dividend_value, 'dividend_percent': dividend_percent,
                                             'last_buy_day': last_buy_day, 'closing_date': closing_date,
                                             'price_one_stock': price_one_stock, 'lot_price': lot_price}
    return sorted(stocks_with_div.items(), key=lambda x: x[1]['dividend_percent'], reverse=True)


def main():
    write_json(get_list_this_year(), 'future_dividends')


if __name__ == '__main__':
    main()
