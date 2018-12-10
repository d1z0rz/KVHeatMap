## NB TODO FIXME
## in order to successfully scrape one page & loop to the next one << suggestions? # TEMP:
## in order to scrape all the results on all pages #I have solve thit problem, look at main_beta.py
## b-c I would like to save them all to a database and analyze

from bs4 import BeautifulSoup
from urllib import request

BASE_URL = 'https://www.kv.ee/?act=search.simple&deal_type=1&search_type=new&parish=1061'
PAGE_SIZE = 1000

def main():
    content = request.urlopen(make_url(BASE_URL, PAGE_SIZE, 1))
    x = count_pages(content)
    print(x)

def make_url(base_url, page_size, page):
    return base_url + '&page_size=%d&page=%d' % (page_size, page)

## https://www.kv.ee/?act=search.simple&page=1&page_size=1000&deal_type=1&
def count_pages(page):
	raw_html = page.read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
	return tag.text


#I have commited, let's add this solution to the main file?
## the thing should be modular, main file should be tiny.
## do you know how to import functions from other files?
## https://stackoverflow.com/a/20309473, ok, now I know
## https://tinyurl.com/now-i-kn0w :DDD
if __name__ == "__main__": ## https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    main()
