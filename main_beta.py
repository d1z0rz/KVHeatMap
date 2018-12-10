from urllib import request
from bs4 import BeautifulSoup
import re
import geocoder

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
result = []
for page_number in range(1, 3):
	## lets extract make_url function into a simple file and import it from there
	## Ok, one question: if previous file was only for counting pages
	## and this file if for creating  database
	## where is the main file?
	## I also have an idea to add to the database all realestates in the country

	## .. *just thinking about modular structure" ..
	## main.py (high-level-abstraction, calls functions, minimal bloat.)
	## url_builder.py
	## extract_page_count.py
	## page_parser.py
	## persistance_layer.py (database related stuff)
	## dublicate_resolver.py
	## convert_data_for_googleMaps.py

	## googleHeatMap init <<< ? = something, which we shold init to show heatmap

	## we are going to need hmm.. API?
	## idea is that when you want to render a google map, you are doing it in a browser
	## thus you need to run google maps in JavaScript and FETCH data from the server

	## (that's how I did it, hmmm I wonder if you could do it in python only
	## I saw a video, where peoples used matplotlib to draw circles on map

	## Link: https://www.youtube.com/watch?v=P60qokxPPZc&t=609s
	## googlemaps package is only for data/responses API. NOT rendering maps.
	## this is the main project idea to prove, that python can do everything
	## https://github.com/rochacbruno/Flask-GoogleMaps <<
	## basically, python code will INJECT javascript into HTML, it won't run on the web
	## although people have been talking about the possibility to run websites not only on
	## HTML CSS JS , but HTML CSS Python or smth, http://www.brython.info/
	## https://github.com/PythonJS/PythonJS

	url = 'https://www.kv.ee/?act=search.simple&last_deal_type=1&page='+str(page_number)+'&orderby=ob&page_size=100&deal_type=1&dt_select=1&county=1&search_type=new&parish=1061'
	print(url)
	content = request.urlopen(url)
	raw_html = content.read()
	soup = BeautifulSoup(raw_html, 'html.parser')

	objects = soup.find_all("tr", class_='object-item')
	for object in objects:
		price_m2 = getPrice(object, PRICE_M2)
		price = getPrice(object, PRICE)
		address = getAddress(object)
		location = getLocation(address)
		result.append({'price':price, 'price_m2':price_m2, 'address':address,'location':location})
print(len(result))
## returns an array of objects [ {coords, address, price, pricem2} ]
