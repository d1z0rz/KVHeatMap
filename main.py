import urllib2

url = 'https://www.kv.ee/?act=search.simple&last_deal_type=1&company_id=&page=1&orderby=ob&page_size=100&deal_type=1&dt_select=1&county=1&search_type=new&parish=1061&rooms_min=&rooms_max=&price_min=&price_max=&nr_of_people=&area_min=&area_max=&floor_min=&floor_max=&energy_certs=&keyword='

content = urllib2.urlopen(url)

res = content.read()

print(res) 
