from typing import Tuple

import requests
import json
import csv
from datetime import date

my_equitys = ('VKCO', 'ALRS', 'BSPB', 'VTBR', 'KRSBP', 'CBOM', 'MAGN', 'MTSS', 'MTLR', 'MOEX', 'NLMK', 'NVTK',
              'OGKB', 'KZOSP', 'POLY', 'RUAL', 'RTKM', 'HYDR', 'SBER', 'CHMF', 'LSRG')


# В переменной my_equitys хранится список акци по которым необходимо собирать накопительную статистику


def get_json():
    """Функция отправляет get запрос к api компании БКС и получет json содержащий актуальную цену по всем акциям
    торгующимся на ММВБ. Информация во время проведения торговой сессии поступает с 15-и минутной задержкой,
     в связи с тем что используется бесплатый api. После завершения торговой сессии информация актуальна на момент
     закрытия торгов. В результаате выполнения функции формируется json файл с информацией по всем акциям, в имени
     файла указывается актуальная дата. После создания файла в терминал выводится сообщение json by all action file
     create"""
    url: str = 'https://api.bcs.ru/partner/quotations?portfolio_ids%5B0%5D=113&portfolio_ids%5B1%5D=114&sorting=1' \
               '&sorting_order=asc&limit=300 '
    headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                   'Safari/537.36',
               'partner-token': 'A5264D52-1510-4E42-8E90-E729FF405646',
               'Accept': '*/*'}

    result = requests.get(url=url, headers=headers).json()
    with open(f'./All_stocks/action_{date.today()}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=True)
    print("json by all action file create")


def pars_json(x):
    """Функция принимает на вход список акций по которым необходимо собирать информацию. Функция открывает файл с
    актуальной информацией по всем акциям и возвращает список словарей с ценой акций на текущую дату"""
    with open(f'./All_stocks/action_{date.today()}.json', 'r', encoding='utf-8') as file:
        equitys_list = json.load(file)
    result = []
    for equity in equitys_list['data']:
        if equity.get("secur_code") in x:
            name = equity.get('issuer')
            close_price = equity.get('close_price')
            date_time = equity.get('last_price_time').split('T')
            price_change_1day_percent = equity.get('price_change_1w_percent')
            result.append({
                'title': name,
                'price': close_price,
                'change price': price_change_1day_percent,
                'date': date_time[0],
            })
        else:
            pass
    return result


def get_result_files(incoming_data):
    """Функция принмает список словарей с информацией по акциям на текущую  дату и формирует два файла: json и csv"""
    with open(f'./My_stocks/my_action_{date.today()}.json', "w", encoding="utf-8") as file:
        json.dump(incoming_data, file, indent=4, ensure_ascii=False)
        print('json file create')
    with open(f'./My_stocks/my_action_{date.today()}.csv', "w", encoding="utf-8") as f:
        w = csv.DictWriter(f, incoming_data[0].keys())
        w.writeheader()
        w.writerows(incoming_data)
        print('csv file create')


def main():
    get_json()
    result_list = pars_json(my_equitys)
    get_result_files(result_list)


if __name__ == '__main__':
    main()
