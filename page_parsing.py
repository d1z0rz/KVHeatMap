from urllib import request
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://www.kv.ee/?act=search.simple&deal_type=1&search_type=new'
PAGE_SIZE = 100
PARISHES = { "tallinn":1061, "parnu":1045, "tartu":1063, 'narva':1036 }

def estimated_time(name):
    url = make_url(name)
    last_number = count_pages(url)
    time = time_calculator(last_number)
    return str(time)

def make_url(name):
    parish = PARISHES[name]
    return BASE_URL + '&page_size=%d&page=%d&parish=%d' % (100, 1, parish)

def count_pages(url):
	content = request.urlopen(url)
	raw_html = content.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
	return int(tag.text)

def time_calculator(last_page):
    opprox_time = last_page*26
    return opprox_time
