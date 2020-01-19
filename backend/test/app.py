from flask import Flask, request, jsonify
import json, os, requests, pymongo
from bson import ObjectId
# from sf_zips import getZips

zips = {
    "SOMA": 94103,
    "Financial District": 94104,
    "The East Cut": 94105,
    "South Park": 94107,
    "Jackson Square": 94108,
    "Russian Hill": 94109,
    "Mission Bay": 94158,
    "Embarcadero": 94111,
    "North Beach": 94133,
    "Marina District": 94123,
    "Pacific Heights": 94115,
    "Lower Pacific Heights": 94117,
    "Presidio": 94129,
    "Outer Richmond": 94121,
    "Richmond District": 94118,
    "Outer Sunset": 94122,
    "Sunset District": 94116,
    "Park Merced": 94132,
    "West Portal": 94127,
    "Twin Peaks": 94131,
    "Noe Valley": 94114,
    "Mission District": 94110,
    "Bayview": 94124,
    "Visitacion Valley": 94134,
    "Outer Mission": 94112,
    "Treasure Island": 94130
}

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = pymongo.MongoClient("mongodb+srv://jeffrey856:cookies1234@safeplatedb-p4xjd.mongodb.net/test?retryWrites=true&w=majority")
app = Flask(__name__)
# zipcodes = getZips()

@app.route('/query', methods=['GET'])
def handle_exact_query():
    args = dict(request.args)
    try:
        projection = {
            'business_name': str(args['name'])
        }
        data = queryMongo(projection)
    except Exception as e:
        print(e)
        return jsonify({"error": 'Error in retrieving data from database.'}), 404
    try:
        res = generate_response(args, data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in generating response for client."}), 404
    return res, 200

@app.route('/like-query', methods=['GET'])
def handle_like_query():
    args = dict(request.args)
    try:
        pattern = args['region']
        projection = {
            'business_postal_code': str(zips[pattern]),
            'business_name': str(args['name'])
        }
        data = queryMongo(projection)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in retrieving data from database."}), 404
    try:
        res = generate_response(args, data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error in generating response for client."}), 404
    return res, 200

def generate_response(args, data):
    tmp = [(str(d), str(data[d])) for d in data]
    print(tmp)
    ret = {
        "data": tmp,
        "parameters": args
    }
    return jsonify(ret)

def queryMongo(projection):
    db = client.restaurants
    col = db.restaurant
    cur = col.find(dict(projection))
    if (cur.count()):
        return cur[0]
    else:
        raise LookupError('Cannot retrieve query:', projection)

if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
