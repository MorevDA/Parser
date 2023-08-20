import json
from pprint import pprint

sorting_options = {0: 'Срок доставки, дней', 1: 'Цена, руб.'}


def get_analog_or_replacement_parts(parts_dict: dict, sorting_option='Цена, руб.') -> dict:
    """ Функция для получения информации по аналогам запчасти, как того же производителя, так и других
    производителей(формат данных в обоих случаях идентичен).
    Функция принимает на вход словарь с 'сырыми' данными полученными в результате скрейпинга сайта.
    Функция возвращает словарь с данными приведенными в удобный для пользователя формат.
    По умолчанию выполняется сортировка по цене, опционально возможно менять параметр сортировки при
    вызове функции."""
    analog = {}
    for i in parts_dict:
        offers = []
        for j in i.get('offers'):
            delivery: int = j['delivery']['value']
            price: float = j['displayPrice']['value']
            amount: int = j['lotQuantity']
            part_info: dict = {'Срок доставки, дней': delivery, 'Цена, руб.': price, 'Количество': amount}
            offers.append(part_info)
        offers.sort(key=lambda x: x[sorting_option])
        analog[f"{i.get('make')} {i.get('detailNum')}"] = offers[: 5]
    return analog


def get_original_parts(parts_list: dict, sorting_option='Цена, руб.') -> list:
    """ Функция для получения информации по запчасти в соответствии с запрошенным номером.
        Функция принимает на вход словарь с 'сырыми' данными полученными в результате скрейпинга сайта.
        Функция возвращает словарь с данными приведенными в удобный для пользователя формат.
        По умолчанию выполняется сортировка по цене, опционально возможно менять параметр сортировки при
        вызове функции."""
    original = []
    for part in parts_list[0]['offers']:
        delivery = part['delivery']['value']
        price = part['displayPrice']['value']
        amount = part['quantity']
        part_info = {'Срок доставки, дней': delivery, 'Цена, руб.': price, 'Доступно для заказа': amount}
        original.append(part_info)
    original.sort(key=lambda x: x[sorting_option])
    return original[:5]


if __name__ == "__main__":
    with open('emex_4475005002_1', 'r', encoding='utf-8') as file:
        search_result = json.load(file)['searchResult']
    print(search_result.keys())
    pprint(get_analog_or_replacement_parts(search_result['analogs']))
