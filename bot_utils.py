import requests


def check_input(message: str):
    data = message.split()
    if len(data) < 2 or not data[0].isdigit():
        raise ValueError(
            'Incorrect input\n'
            'Example: 37260674 Омега 3'
        )
    vendor_code = int(data[0])
    item_name = ' '.join(data[1:]).lower()
    return vendor_code, item_name


def parse_wildberries(vendor_code: int, item_name: str):
    result = []
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/108.0.0.0 Safari/537.36')
    for page in range(1, 101):
        headers = {
            'User-agent': user_agent,
            'Accept': '*/*',
        }
        url = ('https://search.wb.ru/exactmatch/ru/common/v4/search'
               f'?query={item_name}'
               '&resultset=catalog'
               '&sort=popular'
               '&lang=ru'
               '&locale=ru'
               f'&page={page}')
        response = requests.get(url=url, headers=headers)
        json_response = response.json()
        if json_response and vendor_code:
            for pos in range(len(json_response['data']['products'])):
                if (json_response['data']['products'][pos]['id']
                        == vendor_code):
                    result.append('Страница <{}>, позиция <{}>'
                                  .format(page, pos))
    if result:
        return ('Результат поиска товара <{}> с артиклем <{}>'
                .format(item_name, vendor_code) +
                '\n' +
                '\n'.join(result))
    else:
        return 'Товар <{}> с артиклем <{}> не найден'\
            .format(item_name, vendor_code)
