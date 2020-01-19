from flask import Flask, request, jsonify
import json, os, requests, pymongo
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = pymongo.MongoClient("mongodb+srv://jeffrey856:cookies1234@safeplatedb-p4xjd.mongodb.net/test?retryWrites=true&w=majority")
app = Flask(__name__)

@app.route('/query', methods=['GET'])
def endpoint():
	args = dict(request.args)
	try:
		data = queryMongo(args)
	except:
		return jsonify({"error": 'Data not found in database.'}), 404

	print("Query String Args:", args)
	# print("Data retrieved from DB: %s" % data)
	# print(data)
	tmp = [(str(d), str(data[d])) for d in data]

	print(tmp)
	ret = {
		"data": tmp,
		"parameters": args
	}
	return jsonify(ret), 200

# ,'business_address': str(args['address']) if 'address' in args else ""

def queryMongo(args):
	db = client.restaurants
	col = db.restaurant
	projection = {
		'business_name': str(args['name'])
	}
	cur = col.find(projection)
	return cur[0]

if __name__ =='__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
