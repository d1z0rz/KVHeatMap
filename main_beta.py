from urllib import request
from bs4 import BeautifulSoup
import re
import geocoder
import pickle

PRICE = 'object-price-value'
PRICE_M2 = 'object-m2-price'
ADDRESS = 'object-title-a'
BASE_URL = 'https://www.kv.ee/?act=search.simple&deal_type=1&search_type=new&parish=1061'
PAGE_SIZE = 100

result = []
sub_result = []
prices = []

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

def value_with_quotes(figure):
    quoted_value = "'%s'" % figure
    return quoted_value

def make_url(base_url, page_size, page):
    return base_url + '&page_size=%d&page=%d' % (page_size, page)

def count_pages(page):
	raw_html = page.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
	return tag.text

def value_with_quotes(figure):
    quoted_value = "'%s'" % figure
    return quoted_value

def write_list_to_file(guest_list, filename):
    #"""Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in guest_list:
            outfile.write(entries)
            outfile.write("\n")

content = request.urlopen(make_url(BASE_URL, PAGE_SIZE, 1))
last_page_number = count_pages(content)
print(last_page_number)


for page_number in range(1, 2):

	content = request.urlopen(make_url(BASE_URL, PAGE_SIZE, page_number))
	raw_html = content.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	objects = soup.find_all("tr", class_='object-item')
	for object in objects:
		price_m2 = getPrice(object, PRICE_M2)
		#price = getPrice(object, PRICE)
		address = getAddress(object)
		location = getLocation(address)
		if location is not None:
			latitude = location[0]
			longitude = location[1]
			prices.append(price_m2)
			sub_result.append([price_m2, latitude,longitude])
		else:
			print(address,'in not in register yet')

##searching max price in order to calculate weight of the place:
max_price = max(prices)
price_measure_unit = int(max_price/25)

data_file = open('data.txt', 'w')

for element in sub_result:
	weight = int(element[0]/price_measure_unit)
	lat = (element[1])
	lng = (element[2])
	#values_data = str([lat,lng,weight])
	data_file.write(str(lat)+','+str(lng)+','+str(weight)+'\n')
	#result.append([lat,lng,weight])
data_file.close()

##1 min weitgh value and 25 is max weight value
##SO, we need to conver price_m2 to weight
##
## returns an array of objects [ {coords, address, price, pricem2} ]
