import json
import unittest
from resteasy import RESTEasy


api = RESTEasy(endpoint="https://fakesite.com/api", timeout=60)
tasks = api.route("tasks")
tasks.debug = True


class TestCRUD(unittest.TestCase):
    def test_do(self):
        """GET requests"""

        req = tasks.do("GET")
        self.assertEqual(req["endpoint"], "https://fakesite.com/api/tasks")
        self.assertEqual(req["method"], "GET")
        self.assertEqual(req["params"], {})
        self.assertEqual(req["timeout"], 60)

        tasks.timeout = 30
        req = tasks.get()
        self.assertEqual(req["timeout"], 30)
        tasks.timeout = 60

    def test_get(self):
        """GET requests"""

        req = tasks.get(filter="shop")
        self.assertEqual(req["endpoint"], "https://fakesite.com/api/tasks")
        self.assertEqual(req["method"], "GET")
        self.assertEqual(req["params"], {"filter": "shop"})
        self.assertEqual(req["timeout"], 60)

        tasks.timeout = 30
        req = tasks.get()
        self.assertEqual(req["timeout"], 30)
        tasks.timeout = 60

    def test_post(self):
        """POST requests"""

        req = tasks.post(text="test note")
        self.assertEqual(req["endpoint"], "https://fakesite.com/api/tasks")
        self.assertEqual(req["method"], "POST")
        self.assertEqual(req["data"], json.dumps({"text": "test note"}))
        self.assertEqual(req["timeout"], 60)

    def test_put(self):
        """PUT requests"""

        req = tasks.route(1).put(text="test note")
        self.assertEqual(req["endpoint"], "https://fakesite.com/api/tasks/1")
        self.assertEqual(req["method"], "PUT")
        self.assertEqual(req["data"], json.dumps({"text": "test note"}))
        self.assertEqual(req["timeout"], 60)

    def test_patch(self):
        """PATCH requests"""

        req = tasks.route(1).patch(text="test note")
        self.assertEqual(req["endpoint"], "https://fakesite.com/api/tasks/1")
        self.assertEqual(req["method"], "PATCH")
        self.assertEqual(req["data"], json.dumps({"text": "test note"}))
        self.assertEqual(req["timeout"], 60)

    def test_delete(self):
        """DELETE requests"""

        req = tasks.route(1).delete(id=1)
        self.assertEqual(req["endpoint"], "https://fakesite.com/api/tasks/1")
        self.assertEqual(req["method"], "DELETE")
        self.assertEqual(req["params"], {"id": 1})
        self.assertEqual(req["timeout"], 60)


if __name__ == "__main__":
    unittest.main()
