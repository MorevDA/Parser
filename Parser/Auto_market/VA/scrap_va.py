import requests
import json

part_number = 'R3007'

start_params = {
    'term': part_number,
}

ses = requests.Session()
base_url = ses.get('https://www.va36.ru')
cookies = ses.cookies

headers = {
    'authority': 'www.va36.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'authorization=tl_ar_va36; force_stock_id=2; wasid=a4c144009a50c3a09725978698dab03b0646c2df;',
    'referer': 'https://www.va36.ru/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'warlng': 'undefined',
}
data_0 = ses.get('https://www.va36.ru/search/sphinx/', params=start_params, headers=headers, cookies=ses.cookies)
data = ses.get('https://www.va36.ru/search/sphinx/', params=start_params, headers=headers, cookies=ses.cookies)

brand = data.json()[0].get('prd_name')
print(brand)

params = {
    'article': part_number,
    'brand': brand,
    'withAnalogs': '1',
}


def get_content(par: dict, headers: dict, cook) -> object:
    response = ses.get('https://www.va36.ru/api/v2/client/fast-search/',
                       params=par, headers=headers, cookies=cook)
    with open(f"{brand}_{part_number}.json", 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=True)
    print(response.json())


if __name__ == '__main__':
    get_content(params, headers, cookies)
