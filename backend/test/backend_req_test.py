import unittest
import requests

############## Initialize variables ##################

class TestApiRequest(unittest.TestCase):
	def test_get_no_query(self):
		baseurl = 'http://localhost:3000'
		endpoint = '/query'
		params = ''
		response = requests.get(baseurl + endpoint + params)
		response_in_json = response.json()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response_in_json['message'], 'Received query.')
		self.assertEqual(response_in_json['params'], '')

	def test_get_with_query(self):
		baseurl = 'http://localhost:3000'
		endpoint = '/query'
		params = '?search=starbucks'
		response = requests.get(baseurl + endpoint + params)
		response_in_json = response.json()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response_in_json['message'], 'Received query.')
		self.assertEqual(response_in_json['params'], 'starbucks')

if __name__ == '__main__':
	unittest.main()
