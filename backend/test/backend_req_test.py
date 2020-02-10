import unittest
import json
import requests

############## Initialize variables ##################

class TestApiRequest(unittest.TestCase):
	# def test_get_no_query(self):
	# 	print('############# Starting test 1 ###############')
	# 	baseurl = 'http://3da1b925.ngrok.io'
	# 	endpoint = '/query'
	# 	params = ''
	# 	response = requests.get(baseurl + endpoint + params)
	# 	response_in_json = response.json()
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertEqual(response_in_json['data'], {})

	def test_get_with_query(self):
		print('############# Starting test 2 ###############')
		baseurl = 'http://3da1b925.ngrok.io'
		endpoint = '/query'
		params = '?name=starbucks'
		response = requests.get(baseurl + endpoint + params)
		print(response.content.decode('utf-8'))
		# response_in_json = response.json()
		# self.assertEqual(response.status_code, 200)
		# self.assertEqual(response_in_json['message'], 'Received query.')
		# self.assertEqual(response_in_json['params'], 'Starbucks')
		# self.assertFalse('data' not in response_in_json)
		# # print(response_in_json['data'])
		# data = json.loads(response_in_json['data'])
		# for d in data:
		# 	print(d)
		# pretty_data = json.dumps(data, indent=2)
		# print(pretty_data)

	# def test_get_with_query_nonexistent(self):
	# 	print('############# Starting test 3 ###############')
	# 	baseurl = 'http://localhost:3000'
	# 	endpoint = '/query'
	# 	params = 'something'
	# 	response = requests.get(baseurl + endpoint + '?search=' + params)
	# 	response_in_json = response.json()
	# 	print(response_in_json)
	# 	self.assertNotEqual(response.status_code, 200)
	# 	self.assertTrue('error' in response_in_json)
	# 	self.assertEqual(response_in_json['message'], str(params + ' does not exist in DB.'))

if __name__ == '__main__':
	unittest.main()
