import flickr_api
from selenium import webdriver
import requests
import pymongo

conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn.flickr_db  # 连接flickr_db数据库，没有则自动创建
emo_set = db['anger']

api_key = 'your key'
api_secret = 'your secret'

flickr = flickr_api.FlickrAPI(api_key=api_key, api_secret=api_secret)
flickr.use_driver = True

# api_key （必需的）
# Your API application key. See here for more details.
# group_id （必需的）
# The id of the group who's pool you which to get the photo list for.
# tags （可選的）
# A tag to filter the pool with. At the moment only one tag at a time is supported.
# user_id （可選的）
# The nsid of a user. Specifiying this parameter will retrieve for you only those photos that the user has contributed to the group pool.
# extras （可選的）
# A comma-delimited list of extra information to fetch for each returned record. Currently supported fields are: description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o
# per_page （可選的）
# Number of photos to return per page. If this argument is omitted, it defaults to 100. The maximum allowed value is 500.
# page （可選的）
# The page of results to return. If this argument is omitted, it defaults to 1.

# fearof group_id: 34106783@N00 page=1,2
# flickrfear group_id: 1984145@N20 page=1,2,3,4

# joys_of_spring group_id: 306702@N25 page=6,7
# delightfulimages group_id: 2967886@N25 page=1,2,3

# sorrow group_id: 747311@N21 page=1,2
# deafeningsilence group_id: 81026905@N00 page=1,2

# imsoangry group_id: 49072725@N00 page=1,2,3,4

# emotions group_id: 1352909@N24 page=1


for e in flickr.find_all_from_group('49072725@N00', page='4'):
    print(e)
    if e:
        emo_set.insert(e)

flickr.die()

if __name__ == '__main__':
    pass
