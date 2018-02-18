from bs4 import BeautifulSoup
from Spiders.tools import *

# steam
base = 'http://steamcommunity.com/market/search?category_570_Hero[]=any&category_570_Slot[]=any&category_570_Type[]=any&appid=570&l=schinese&q='
requests.session().keep_alive = False


def main():
    # print(get_steam_price('一艘小船'))
    pass


def get_price(item_name):
    url = base + item_name
    html = get_page(url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        result = soup.find(id='resultlink_0')
        if result is not None:
            name = result.find(id='result_0_name').text
            price_text = result.findAll(attrs={'class', 'normal_price'})[1].text
            if name == item_name:
                return price_text


if __name__ == '__main__':
    main()
