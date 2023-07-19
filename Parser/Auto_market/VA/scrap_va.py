import requests
import json


def get_content(par: dict, head: dict, cook, brand: str, p_number: str) -> object:
    response = req.get('https://www.va36.ru/api/v2/client/fast-search/',
                       params=par, headers=head, cookies=cook)
    with open(f"{brand}_{p_number}_1.json", 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=True)
    print(response.json())


part_number = 'R3007'
urls = {'base_search_url': 'https://www.va36.ru/search/sphinx/',
       'reserve_search_url': 'https://www.va36.ru/api/v2/client/fast-search/'}

params = {'start_params_base': {'term': part_number},
          'start_params_reserve': {'article': part_number, 'withAnalogs': '1'}}

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

req = requests.Session()
cookies = req.get('https://www.va36.ru', headers=headers).cookies


data_0 = req.get(url=urls['reserve_search_url'], params=params['start_params_reserve'],
                 headers=headers, cookies=cookies)
data = req.get(url=urls['reserve_search_url'], params=params['start_params_reserve'],
               headers=headers, cookies=cookies)

brand = data.json().get('data').get('brands')[0]['name']
print(brand)

params_for_total = {'article': part_number, 'brand': brand, 'withAnalogs': '1',}



if __name__ == '__main__':
    get_content(params_for_total, headers, cookies, brand, part_number)
