#!/home/chad/Code/tmobile/tmobile_venv/bin/python3

import requests
import unittest

def get_url():
    req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
    response_data = req.json()

    return (req.status_code, response_data)

class TestServer(unittest.TestCase):
    TEST_URL = 'http://www.google.com/'

    def test_url_shorten(self):
        print(f'DEBUG: test_url_shorten')
        req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
        response_data = req.json()

        self.assertEqual(req.status_code, 200)
        self.assertTrue('url' in response_data)

        print(f'DEBUG: {response_data}')

    def test_no_duplicates(self):
        print(f'DEBUG: test_no_duplicates')
        req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
        response_data = req.json()

        shortened_url = response_data['url']

        req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
        response_data = req.json()

        next_shortened_url = response_data['url']

        self.assertEqual(shortened_url, next_shortened_url)

    def test_redirect(self):
        print(f'DEBUG: test_redirect')

        req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
        response_data = req.json()

        shortened_url = response_data['url']

        redirect_req = requests.get(shortened_url)

        self.assertEqual(req.status_code, 200)

    def test_invalid_url_uid(self):
        print(f'DEBUG: test_invalid_url_uid')
        req = requests.get(f'http://localhost:5000/a')
        response_data = req.json()

        self.assertEqual(req.status_code, 404)
        self.assertTrue('message' in response_data)
        self.assertEqual(response_data.get('message'), 'URL UID does not exist')

    def test_hit_counter(self):
        req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
        response_data = req.json()
        hits = response_data['hits']
        shortened_url = response_data['url']

        requests.get(shortened_url)

        req = requests.get(f'http://localhost:5000/?url={TestServer.TEST_URL}')
        response_data = req.json()
        next_hits = response_data['hits']

        self.assertEqual(int(next_hits) - int(hits), 1)

if __name__ == '__main__':
    unittest.main()
