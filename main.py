from urllib import request
from bs4 import BeautifulSoup
import re
import geocoder
import time
u = time.time()

PRICE = 'object-price-value'
PRICE_M2 = 'object-m2-price'
ADDRESS = 'object-title-a'

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
url = 'https://www.kv.ee/?act=search.simple&last_deal_type=1&page=2&orderby=ob&page_size=500&deal_type=1&dt_select=1&county=1&search_type=new&parish=1061'
content = request.urlopen(url)
raw_html = content.read()
soup = BeautifulSoup(raw_html, 'html.parser')

objects = soup.find_all("tr", class_='object-item')
result = []
for object in objects:
	price_m2 = getPrice(object, PRICE_M2)
	price = getPrice(object, PRICE)
	address = getAddress(object)
	location = getLocation(address)
	result.append({'price':price, 'price_m2':price_m2, 'address':address,'location':location})
#print(result)
u2 = time.time()
kek = u2 - u
print(kek)
## returns an array of objects [ {coords, address, price, pricem2} ]
