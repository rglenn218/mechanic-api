import unittest

from config import TestingConfig
from application import create_app
from application.extensions import db
from application.models import Customer

class CustomerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            customer = Customer(
                name="Test Customer",
                email="test@example.com",
                phone="5551234567",
                password="password123"
            )
            
            db.session.add(customer)
            db.session.commit()
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def get_customer_token(self):
        response = self.client.post(
            "/customers/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        data = response.get_json()
        return data["token"]
            
    def test_create_customer(self):
        response = self.client.post(
            "/customers/",
            json={
                "name": "Rachel Glenn",
                "email": "rachel@example.com",
                "phone": "5559876543",
                "password": "password123"
            }
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = response.get_json()
        
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], "Rachel Glenn")
        self.assertEqual(data["email"], "rachel@example.com")
        
    def test_get_all_customers(self):
        response = self.client.get("/customers/?page=1&per_page=5")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn("customers", data)
        self.assertEqual(len(data["customers"]), 1)
        
    def test_get_customer_by_id(self):
        response = self.client.get("customers/1")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Test Customer")
        self.assertEqual(data["email"], "test@example.com")
        
    def test_get_customer_not_found(self):
        response = self.client.get("/customers/999")
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Customer not found")
        
    def test_customer_login(self):
        response = self.client.post(
            "/customers/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["message"], "Login successful")
        self.assertIn("token", data)
        
    def test_customer_login_invalid_password(self):
        response = self.client.post(
            "/customers/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        
        self.assertEqual(response.status_code, 401)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Invalid email or password")
        
    def test_update_customer(self):
        token = self.get_customer_token()
        
        response = self.client.put(
            "/customers/1",
            json={
                "phone": "5551112222"
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["phone"], "5551112222")
        
    def test_update_customer_missing_token(self):
        response = self.client.put(
            "/customers/1",
            json={
                "phone": "5551112222"
            }
        )
        
        self.assertEqual(response.status_code, 401)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Token is missing")
        
    def test_delete_customer(self):
        token = self.get_customer_token()
        
        response = self.client.delete(
            "/customers/1",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["message"], "Customer deleted successfully")