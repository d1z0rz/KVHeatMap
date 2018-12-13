from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from tinydb import TinyDB, Query

db = TinyDB('data.json')

app = Flask(__name__)
api = Api(app)

MAX_WEIGHT = 25
def calculate_weight(price, max_price, max_weight):
    return int( round( (price / max_price) * max_weight ) )

def find_max_price(query_results, price_type='price_m2'):
    all_prices = []
    for result in query_results:
        price = result[price_type]
        all_prices.append(price)
    if not all_prices:
        return 0
    return max(all_prices)

class Heatmap_Data(Resource):
    def get(self):
        response = []
        Estate = Query()
        query_results = db.search(Estate.parish == 1061)
        max_price_m2 = find_max_price(query_results, 'price_m2')
        for result in query_results :
            weight = calculate_weight(result['price_m2'], max_price_m2, MAX_WEIGHT)
            lat = result['latitude']
            lng = result['longitude']
            response.append({'weight': weight, 'latitude': lat, 'longitude': lng })
        return jsonify(response)


api.add_resource(Heatmap_Data, '/test')

if __name__ == '__main__':
     app.run()
