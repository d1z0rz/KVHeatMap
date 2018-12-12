from urllib import request
from bs4 import BeautifulSoup
import re
import geocoder
import pickle
from tinydb import TinyDB

	##searching max price in order to calculate weight of the place:
	# max_price = max(prices)
	# price_measure_unit = int(max_price/25)

PRICE = 'object-price-value'
PRICE_M2 = 'object-m2-price'
ADDRESS = 'object-title-a'
BASE_URL = 'https://www.kv.ee/?act=search.simple&deal_type=1&search_type=new'
PAGE_SIZE = 1000
PARISHES = { "tallinn":1061, "parnu":1045, "tartu":1063, 'narva':1036 }
db = TinyDB('data.json')

def main():
	scrape_parish('tallinn')

def scrape_parish(name):
	parish = PARISHES[name]
	if (parish is None):
		raise ValueError('Parish "%s" not found' % (parish))
	url = make_url(BASE_URL, PAGE_SIZE, 1, parish)
	last_page_number = count_pages(url)
	for page_number in range(1): ## TODO
		url = make_url(BASE_URL, PAGE_SIZE, page_number, parish)
		estate_objects = parse_page(url)
		save_to_db(estate_objects, parish)

def save_to_db(objects, parish):
	for object in objects:
		object['parish'] = parish
		db.insert(object)

def parse_page(url):
	content = request.urlopen(url)
	raw_html = content.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	objects = soup.find_all("tr", class_='object-item')
	return parse_objects(objects)

def parse_objects(objects):
	results = []
	for object in objects:
		result = parse_object(object)
		if (result is not None):
			results.append(result)
	return results

def parse_object(object):
	price_m2 = getPrice(object, PRICE_M2)
	price = getPrice(object, PRICE)
	address = getAddress(object)
	location = getLocation(address)
	if location is not None:
		latitude = location[0]
		longitude = location[1]
		object = {'address':address, 'price': price, 'price_m2':price_m2, 'latitude': latitude, 'longitude':longitude}
		return object
	else:
		print(address,'in not in register yet')

def getPrice(tag, type):
	res = tag.find(class_=type)
	raw_text = res.text
	return format_price(raw_text)

def format_price(raw_price):
	stripped = raw_price.strip().replace(u'\xa0', '')
	formatted = re.findall(r'\d+', stripped)
	return int(formatted[0])

def getAddress(tag):
	res = tag.find(class_=ADDRESS)
	raw_text = res.text
	stripped = raw_text.strip()
	array = stripped.split(", ")
	return array[1] + ', ' + array[-1]

def getLocation(address):
	raw_address = geocoder.yandex(address)
	location = raw_address.latlng
	return location

def make_url(base_url, page_size, page, parish):
    return base_url + '&page_size=%d&page=%d&parish=%d' % (page_size, page, parish)

def count_pages(url):
	content = request.urlopen(url)
	raw_html = content.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
	return tag.text

if (__name__ == "__main__"):
	main()
