import json
import requests
import unittest

import time

with open("../config.json") as json_data:
    config = json.load(json_data)

host = str(config["host"])
port = str(config["port"])
url_create = 'http://' + host + ':' + port + '/api/session/create'
url_load = 'http://' + host + ':' + port + '/api/session/load'
url_renew = 'http://' + host + ':' + port + '/api/session/renew'
url_delete = 'http://' + host + ':' + port + '/api/session/delete'

headers = {'content-type': 'application/json'}


class MyTest(unittest.TestCase):
    existing_session_id = "blank"

    def setUp(self):
        payload = {"userId": "test@test"}
        self.existing_session_id = requests.post(url_create, data=json.dumps(payload), headers=headers).text

    def tearDown(self):
        requests.post(url_delete, data=self.existing_session_id, headers=headers)

    def test_session_create(self):
        payload = {"userId": "test@test"}
        r = requests.post(url_create, data=json.dumps(payload), headers=headers)
        existing_session_id = r.text
        self.assertNotEqual(existing_session_id, "blank")

    def test_session_load(self):
        r = requests.post(url_load, data=self.existing_session_id, headers=headers)
        response = r.json()
        payload = {"userId": "test@test"}
        self.assertEqual(response, payload)

    def test_not_existing_session_load(self):
        payload = {"sessionId": "notexistingsession"}
        r = requests.post(url_load, data=json.dumps(payload), headers=headers)
        response = r.json()
        payload = {"userId": None}
        self.assertEqual(response, payload)

    def test_session_renew(self):
        r = requests.post(url_renew, data=self.existing_session_id, headers=headers)
        response = r.json()
        success = {"success": True}
        self.assertEqual(response, success)

    def test_not_existing_session_renew(self):
        payload = {"sessionId": "notexistingsession"}
        r = requests.post(url_renew, data=json.dumps(payload), headers=headers)
        response = r.json()
        success = {"success": False}
        self.assertEqual(response, success)

    def test_session_delete(self):
        r = requests.post(url_delete, data=self.existing_session_id, headers=headers)
        response = r.json()
        success = {"success": True}
        self.assertEqual(response, success)

    def test_delete_not_existing_session(self):
        payload = {"sessionId": "notexistingsession"}
        r = requests.post(url_delete, data=json.dumps(payload), headers=headers)
        response = r.json()
        success_false = {"success": False}
        self.assertEqual(response, success_false)

    @unittest.skip("uncomment this line for session expire testing")
    def test_session_expire(self):
        payload = {"userId": "test@test"}
        session_id = requests.post(url_create, data=json.dumps(payload), headers=headers).text
        time.sleep(5)
        response = requests.post(url_renew, data=session_id, headers=headers).json()
        success_false = {"success": False}
        self.assertEqual(response, success_false)

    @unittest.skip("uncomment this line for session expire testing")
    def test_load_expire(self):
        payload = {"userId": "test@test"}
        session_id = requests.post(url_create, data=json.dumps(payload), headers=headers).text
        time.sleep(5)
        response = requests.post(url_load, data=session_id, headers=headers).json()
        success_false = {"userId": None}
        self.assertEqual(success_false, response)


if __name__ == '__main__':
    unittest.main()
