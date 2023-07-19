import json
from pprint import pprint


def get_json():
    """Функция для чтения json файла"""
    with open('VALEO_R3007_1.json', 'r', encoding='UTF-8') as data_file:
        all_parts_list = json.load(data_file)
    return all_parts_list


def get_original_parts(parts):
    """Функция для сотавления словаря с оригинальными з/x. На вход функции поступает словарь с данными
    по оригинальным з/x и аналогам. Функция возвращает словарь требуемого формата только с оригинальными з/ч.
    Исходящий словарь отсортирован по возрастанию цены"""
    originals = {}
    original_parts = parts.get('data').get('rows').get('request')
    for j, i in enumerate(original_parts):
        originals[j] = {'estimated_delivery_days': i.get('termMax'), ' estimated_delivery_date': i.get('termDate'),
                        'price': i.get('price'), 'amount': i.get('amount'), 'seller': i.get("destination"),
                        'seller_rank': i.get('rating')}
    return sorted(originals.items(), key=lambda x: x[1]['price'])


def get_analog_parts(parts):
    """Функция для сотавления словаря с аналогами запасных частей. На вход функции поступает словарь с данными
        по оригинальным з/ч и аналогам. Функция возвращает словарь требуемого формата только с аналогами."""
    analog = {}
    analog_parts = parts.get('data').get('rows').get('nonOriginalAnalog')
    for part in analog_parts:
        delivery_days = part.get('termMax')
        article = part.get('article')
        brand = part.get('brand')
        name = part.get('name')
        price = part.get('price')
        amount = part.get('amount')
        date_delivery = part.get('termDate')
        destination = part.get("destination");
        offers = {'estimated_delivery_days': delivery_days,  'estimated_delivery_date': date_delivery,
                  'amount': amount, 'price': price, 'vendor': destination}
        if article not in analog:
            analog[article] = {'brand_name': brand, 'part_name': name, 'offers_list': [offers]}
        else:
            analog[article]['offers_list'].append(offers)
    return analog


if __name__ == '__main__':
    x = get_json()
    pprint(get_original_parts(x))
    pprint(get_analog_parts(x))




