import json
from datetime import date


file_name = 'my_stock_information'
name_file_by_date = f'./My_stocks/my_action_{date.today()}'


def read_json_file(f_name: str) -> dict:
    with open(f'{f_name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_update_dict(last_day_course: dict, result_dict: dict) -> dict:
    for j in last_day_course:
        if j['title'] not in result_dict:
            result_dict[j['title']] = {f"price at {j['date']}": j['price']}
        else:
            result_dict[j['title']].update({f"price at {j['date']}": j['price']})
    return result_dict


def get_actualisation_fail(f_name: str, inp_dict: dict) -> None:
    with open(f'{f_name}.json', 'w', encoding='utf-8') as file:
        json.dump(inp_dict, file, indent=4, ensure_ascii=False)
    print('file_update')


if __name__ == '__main__':
    my_stocks_dict_all_date = read_json_file(file_name)
    my_stocks_date_today = read_json_file(name_file_by_date)
    result = get_update_dict(my_stocks_date_today, my_stocks_dict_all_date)
    get_actualisation_fail(file_name, result)


