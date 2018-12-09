import geocoder

def getLocation(address):
	geocode_raw = geocoder.yandex(address)[0]
	print(geocode_raw.latlng)
	return geocode_raw
print(getLocation('Kastani 19, Tallinn'))	
