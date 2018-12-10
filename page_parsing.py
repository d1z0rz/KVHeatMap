## find the element on the HTML page that contains queue results
## find how many results there are total for the given city (i.e parish 1061 aka TALLINN)
## in order to have a starting page and calculate ending page
## in order to successfully scrape one page & loop to the next one
## in order to scrape all the results on all pages
## b-c I would like to save them all to a database and analyze

from bs4 import BeautifulSoup
from urllib import request

BASE_URL = 'https://www.kv.ee/?act=search.simple&deal_type=1&search_type=new&parish=1061'
PAGE_SIZE = 1000

def make_url(base_url, page_size, page):
    return base_url + '&page_size=%d&page=%d' % (page_size, page)

## https://www.kv.ee/?act=search.simple&page=1&page_size=1000&deal_type=1&
def count_pages(page):
	raw_html = page.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
	return tag.text

content = request.urlopen(make_url(BASE_URL, PAGE_SIZE, 1))
x = count_pages(content)
print(x)
#raw_html = content.read()
#soup = BeautifulSoup(raw_html, 'html.parser')
#tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
#print(tag.text)
## 'Only the following pseudo-classes are implemented: nth-of-type.
##.jump-pagination-list > li:nth-last-child(2)
## working fine
