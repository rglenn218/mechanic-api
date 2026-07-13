import unittest

from config import TestingConfig
from application import create_app
from application.extensions import db
from application.models import Mechanic

class MechanicTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            mechanic = Mechanic(
                name="Test Mechanic",
                email="mechanic@example.com",
                password="password123",
                phone="5559876543",
                salary=75000
            )
            
            db.session.add(mechanic)
            db.session.commit()
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def get_mechanic_token(self):
        response = self.client.post(
            "/mechanics/login",
            json={
                "email": "mechanic@example.com",
                "password": "password123"
            }
        )
        
        data = response.get_json()
        return data["token"]
    
    def test_create_mechanic(self):
        response = self.client.post(
            "/mechanics/",
            json={
                "name": "Arthur Fonzarelli",
                "email": "thefonz@mechanics.com",
                "password": "password123",
                "phone": "5551112222",
                "salary": 80000
            }
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = response.get_json()
        
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], "Arthur Fonzarelli")
        self.assertEqual(data["email"], "thefonz@mechanics.com")
        
    def test_mechanic_login(self):
        response = self.client.post(
            "/mechanics/login",
            json={
                "email": "mechanic@example.com",
                "password": "password123"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["message"], "Mechanic login successful")
        self.assertIn("token", data)
        
    def test_mechanic_login_invalid_password(self):
        response = self.client.post(
            "/mechanics/login",
            json={
                "email": "mechanic@example.com",
                "password": "wrongpassword"
            }
        )
        
        self.assertEqual(response.status_code, 401)
        
        data= response.get_json()
        
        self.assertEqual(data["error"], "Invalid email or password")
        
    def test_get_all_mechanics(self):
        response = self.client.get("/mechanics/")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Mechanic")
        
    def test_get_mechanic_by_id(self):
        response = self.client.get("/mechanics/1")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Test Mechanic")
        
    def test_get_mechanic_not_found(self):
        response = self.client.get("/mechanics/999")
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Mechanic not found")
        
    def test_get_mechanics_by_most_tickets(self):
        response = self.client.get("/mechanics/most-tickets")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertIsInstance(data, list)
        
    def test_update_mechanic(self):
        token = self.get_mechanic_token()
        
        response = self.client.put(
            "/mechanics/1",
            json={
                "salary": 82000
            },
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["salary"], 82000)
        
    def test_update_mechanic_missing_token(self):
        response = self.client.put(
            "/mechanics/1",
            json={
                "salary": 82000
            }
        )
        
        self.assertEqual(response.status_code, 401)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Token is missing")
        
    def test_delete_mechanic(self):
        token = self.get_mechanic_token()
        
        response = self.client.delete(
            "/mechanics/1",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["message"], "Mechanic deleted successfully")
        
if __name__ == "__main__":
    unittest.main()