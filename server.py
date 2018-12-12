from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
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



#class Departmental_Salary(Resource):
#    def get(self, department_name):
#        conn = e.connect()
#        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
#        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
#        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#        return result
#        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient

#api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Heatmap_Data, '/test')

if __name__ == '__main__':
     app.run()
