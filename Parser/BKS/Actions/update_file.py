import json
from datetime import date
from pprint import pprint

today = date.today()
file_name = 'my_stocks_information'


def get_full_stocks_list(f_name: str) -> dict:
    with open(f'{f_name}.json', 'r', encoding='utf-8') as f:
        start_data = json.load(f)
    return start_data


def get_information_by_date(date: str, result):
    with open(f'./My_stocks/my_action_{date}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for j in data:
            if j['title'] not in result:
                result[j['title']] = {f"price at {j['date']}": j['price']}
            else:
                result[j['title']].update({f"price at {j['date']}": j['price']})
    return result


def get_actualisation_fail(x):
    with open('my_stock_information.json', 'w', encoding='utf-8') as file:
        json.dump(x, file, indent=4, ensure_ascii=False)
    print('file_update')


def main():
    get_actualisation_fail(get_information_by_date(today, get_full_stocks_list()))

if __name__ == '__main__':
    main()
