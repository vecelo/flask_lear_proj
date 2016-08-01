import unittest
from main import app
import json
from mockito import *

class FlaskLoginMixin(object):
    LOGIN_URL = "/login/"
    LOGOUT_URL = "/logout/"
    
    def login (self, email, password):
        return self.app.post(self.LOGIN_URL, data={
            "email": email,
            "password": password
        }, follow_redirects=True)
        
    def logout (self):
        return self.app.get(self.LOGOUT_URL, follow_redirects=True)

        
class ExampleFlaskTest(unittest.TestCase, FlaskLoginMixin):
    def setUp(self):
        self.app = app.test_client()
    
    def test_login(self):
        response = self.login("me@example.com", "secret")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Success" in response.data)
        
    def test_failed_login(self):
        response = self.login("admin", "PASSWORD")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invalid" in response.data)
        
    def test_logout(self):
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("logged out" in response.data)
        
class ExampleFlaskTest(unittest.TestCase, FlaskLoginMixin):
    def setUp(self):
        self.app = app.test_client()
        
    def test_admin_can_get_to_admin_page(self):
        self.login("me@example.com", "secret")
        response = self.app.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Hello" in response.data)
        
    def test_non_logged_in_user_can_get_to_admin_page(self):
        response = self.app.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("redirected" in response.data)
         
    def test_normal_user_cannot_get_to_admin_page(self):
        self.login("user", "password")
        response = self.app.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("redirected" in response.data)
         
    def test_logging_out_prevents_access_to_admin_page(self):
        self.login("me@example.com", "secret")
        self.logout()
        response = self.app.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("redirected" in response.data)

class ExampleFlaskAPITest(unittest.TestCase, FlaskLoginMixin):
    def setUp(self):
        self.app = app.test_client()
        self.comment_data = {
            "name": "admin",
            "email": "admin@example.com",
            "url": "http://localhost",
            "ip_address": "127.0.0.1",
            "body": "test comment!",
            "entry_id": 1
        }
        
    def test_adding_comment(self):
        response = self.app.post("/api/comment",
            data=json.dumps(self.comment_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue("body" in response.data)
        self.assertEqual(json.loads(response.data)['body'], self.comment_data['body'])
        
    def test_getting_comment(self):
        result = self.app.post("/api/comment",
            data=json.dumps(self.comment_data), content_type="application/json")
        response = self.app.get("/api/comment")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(result.data) in json.loads(response.data)['objects'])
        

class FlaskExampleTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = mock()
        def get_fake_db():
            return self.db
        app.get_db = get_fake_db
        
    def test_before_request_override(self):
        when(self.db).get("foo").thenReturn("123")
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "123")


if __name__ == "__main__":
    unittest.main()
