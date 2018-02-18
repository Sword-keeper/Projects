from Spiders.tools import *

requests.session().keep_alive = False
base = 'http://www.dotasell.com/xhr/json_search.ashx'


def get_item(item_name):
    req_data = {
        'appid': '570',
        'keyw': item_name,
        'Sockets': '0',
        'start': '0',
        'fuzz': 'true',
        'AssetsType': '0',
        'OrderBy': 'Default',
        'safeonly': 'false'
    }
    response = get_response(generate_url(req_data, base))
    if response:
        data = response.json()
        if data and 'MerchandiseList' in data:
            items = data.get('MerchandiseList')
            for item in items:
                name = item.get('LocalName')
                if name.replace(' ', '') == item_name.replace(' ', ''):
                    return item


def for_all_items(do_function=do_nothing):
    req_data = {
        'Sockets': '0',
        'start': '0',
        'AssetsType': '0',
        'OrderBy': 'Default',
        'AppID': '570',
        'safeonly': 'false'
    }
    start = 0
    while True:
        req_data['start'] = str(start)
        start = start + 80
        url = generate_url(req_data, base)
        response = get_response(url)
        if response:
            data = response.json()
            if data and 'MerchandiseList' in data:
                items = data.get('MerchandiseList')
                if len(items) < 1:
                    break
                for item in items:
                    do_function(item)
                continue
        break


def main():
    # for_all_items(do something here)
    pass


if __name__ == '__main__':
    main()
