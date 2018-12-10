## find the element on the HTML page that contains queue results
## find how many results there are total for the given city (i.e parish 1061 aka TALLINN)
## in order to have a starting page and calculate ending page
## in order to successfully scrape one page & loop to the next one
## in order to scrape all the results on all pages
## b-c I would like to save them all to a database and analyze

from bs4 import BeautifulSoup
from urllib import request

url = 'https://www.kv.ee/?act=search.simple&last_deal_type=1&page=2&orderby=ob&page_size=100&deal_type=1&dt_select=1&county=1&search_type=new&parish=1061'
content = request.urlopen(url)
raw_html = content.read()
soup = BeautifulSoup(raw_html, 'html.parser')
tag = soup.select('.jump-pagination-list > li:nth-of-type(3)')[0]
print(tag.text)
## 'Only the following pseudo-classes are implemented: nth-of-type.
##.jump-pagination-list > li:nth-last-child(2)
## working fine
