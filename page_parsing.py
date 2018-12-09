from bs4 import BeautifulSoup
from urllib import request

url = 'https://www.kv.ee/?act=search.simple&last_deal_type=1&page=2&orderby=ob&page_size=100&deal_type=1&dt_select=1&county=1&search_type=new&parish=1061'
content = request.urlopen(url)
raw_html = content.read()
soup = BeautifulSoup(raw_html, 'html.parser')
page_number_html = soup.find_all('div', class_="pagination")

def page_number_finder(tag):
	numbers = tag.find(class_="active")
	print(numbers)
	return numbers

page_number_finder(page_number_html)
