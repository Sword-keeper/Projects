from urllib.parse import urlencode
import requests
import time
from multiprocessing.pool import Pool

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import TimeoutError

ENTRY_TIME = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
DOWNLOAD_LOG_ON = False
MONGO_LOG_ON = False
MULTIPROCESS_LOG_ON = False


class WebDriver:
    driver = None

    @property
    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        return webdriver.WebDriver(chrome_options=chrome_options)

    def __init__(self):
        self.driver = self._init_driver

    def get(self, url):
        self.driver.get(url)


def download(param=None, url=None, file_path=None):
    if param:
        url = param['url']
        file_path = param['path']
    if DOWNLOAD_LOG_ON:
        print(f'Downloading {url} # as', file_path)
    try:
        response = get_response(url)
        with open(file_path, 'wb') as f:
            f.write(response.content)
            f.flush()
    except:
        if DOWNLOAD_LOG_ON:
            print(f'Failed to download {url} # as', file_path)
        return


def do_nothing(param):
    pass


def generate_url(req_data, base):
    params = urlencode(req_data)
    return base + '?' + params


def get_response(url, header=None, proxies=None, timeout=300):
    try:
        with requests.get(url, headers=header, proxies=proxies, timeout=timeout) as response:
            return response
    except TimeoutError:
        print(f'timeout_getting_response: url={url}')


def get_page(url, header=None, proxies=None):
    response = get_response(url, header=header, proxies=proxies)
    if response and response.status_code == 200:
        return response.text


def save_to_mongo(result, db, table_name='default'):
    if db[table_name].insert(result):
        if MONGO_LOG_ON:
            print(f'Successfully saved to Mongodb {table_name} #', result)
        return True
    return False


def update_mongo(where_stmt, update_stmt, db, table_name='default'):
    if db[table_name].update(where_stmt, update_stmt):
        if MONGO_LOG_ON:
            print('Successfully updated Mongo #', update_stmt)
        return True
    return False


def find_by_class(soup, class_name):
    return soup.find(attrs={'class': class_name})


def find_all_by_class(soup, class_name):
    return soup.findAll(attrs={'class': class_name})


def multi_process(do_function, params=None, processes=4):
    if MULTIPROCESS_LOG_ON:
        print(f'Pool ready,{processes} processes on')
    pool = Pool(processes)
    pool.map(do_function, params)
    pool.close()
    pool.join()
    if MULTIPROCESS_LOG_ON:
        print('Pool joined!')


def load_list(file_name='url_list.txt'):
    with open(file_name, 'r') as f:
        urls = [x.strip('\n') for x in f.readlines()]
        return urls


def save_list(url, file_name='url_list.txt'):
    with open(file_name, 'a+') as f:
        f.write(url + '\n')
