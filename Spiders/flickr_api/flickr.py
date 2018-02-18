import json
from urllib.parse import urlencode
from selenium import webdriver
import requests
from selenium.webdriver.chrome.options import Options


class FlickrAPI:
    defaults = dict()
    defaults['api_key'] = None
    defaults['api_secret'] = None
    defaults['header'] = {
        'Accept-Encoding': 'br, gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
                      'Version/11.0.2 Safari/604.4.7',
        'Host': 'api.flickr.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn'
    }

    api_key = None
    api_secret = None
    header = None
    api_base = 'https://api.flickr.com/services/rest/'
    driver = None
    use_driver = False

    @property
    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        return webdriver.Chrome(chrome_options=chrome_options)

    def __init__(self, api_key=defaults['api_key'], api_secret=defaults['api_secret'], header=defaults['header']):
        self.api_key = api_key
        self.api_secret = api_secret
        self.header = header
        self.driver = self._init_driver

    def find_all_from_group(self, group_id, page=1):
        json_data = self.do_flickr_call(method='flickr.groups.pools.getPhotos', format='json',
                                        extras='url_c', group_id=group_id, page=page)
        data = json.loads(json_data)
        photos = data['photos']['photo']
        for photo in photos:
            try:
                pid = photo['id']
                title = photo['title']
                if 'url_c' in photo:
                    url = photo['url_c']
                else:
                    farm = photo['farm']
                    server = photo['server']
                    secret = photo['secret']
                    url = f'https://farm{farm}.staticflickr.com/{server}/{pid}_{secret}.jpg'
                ele = {
                    'id': pid,
                    'title': title,
                    'url': url,
                    'tags': self.get_tags(pid),
                    'comments': self.get_comments(pid)
                }
                yield ele
            except:
                print(f'failed to get photo with id[{pid}]')
                yield None

    def get_tags(self, photo_id):
        json_data = self.do_flickr_call(method='flickr.tags.getListPhoto', photo_id=photo_id, format='json')
        data = json.loads(json_data)
        tags = [x['_content'] for x in data['photo']['tags']['tag']]
        return tags

    def get_comments(self, photo_id):
        json_data = self.do_flickr_call(method='flickr.photos.comments.getList', photo_id=photo_id, format='json')
        data = json.loads(json_data)
        if 'comment' in data['comments']:
            comments = [x['_content'] for x in data['comments']['comment']]
            return comments

    def get_title(self, photo_id):
        json_data = self.do_flickr_call(method='flickr.photos.getInfo', photo_id=photo_id, format='json')
        data = json.loads(json_data)
        try:
            title = data['photo']['title']['_content']
            return title
        except Exception:
            return None

    def do_flickr_call(self, timeout=None, **kwargs):
        params = kwargs.copy()
        if 'jsoncallback' not in params:
            params['nojsoncallback'] = 1
        if self.use_driver:
            return self._flickr_call_with_driver(**params)
        else:
            return self._flickr_call(timeout, **params)

    def _generate_url(self, req_data):
        req_data['api_key'] = self.api_key
        req_data['api_secret'] = self.api_secret
        params = urlencode(req_data)
        url = self.api_base + '?' + params
        return url

    def _flickr_call(self, timeout, **params):
        reply = requests.get(self._generate_url(params), timeout=timeout, headers=self.header)
        return reply

    def _flickr_call_with_driver(self, **params):
        url = self._generate_url(params)
        self.driver.get(url)
        reply = self.driver.find_element_by_tag_name('pre').text
        return reply

    def die(self):
        print('flickrapi terminated')
        self.driver.close()
