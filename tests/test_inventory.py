import unittest

from config import TestingConfig
from application import create_app
from application.extensions import db
from application.models import Inventory

class InventoryTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            part = Inventory(
                name="Brake Pads",
                price=89.99
            )
            
            db.session.add(part)
            db.session.commit()
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all
            
    def test_create_inventory_item(self):
        response = self.client.post(
            "/inventory/",
            json={
                "name": "Oil Filter",
                "price": 19.99
            }
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = response.get_json()
        
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["name"], "Oil Filter")
        self.assertEqual(data["price"], 19.99)
        
    def test_create_inventory_item_invalid_data(self):
        response = self.client.post(
            "/inventory/",
            json={
                "name": "Oil Filter"
            }
        )
        
        self.assertEqual(response.status_code, 400)
        
    def test_get_all_inventory(self):
        response = self.client.get("/inventory/")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Brake Pads")
        
    def test_get_inventory_item_by_id(self):
        response = self.client.get("/inventory/1")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Brake Pads")
        self.assertEqual(data["price"], 89.99)
        
    def test_get_inventory_item_not_found(self):
        response = self.client.get("/inventory/999")
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Inventory item not found")
        
    def test_update_inventory_item(self):
        response = self.client.put(
            "/inventory/1",
            json={
                "price": 99.99
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["price"], 99.99)
        
    def test_update_inventory_item_not_found(self):
        response = self.client.put(
            "/inventory/999",
            json={
                "price": 99.99
            }
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Inventory item not found")
        
    def test_delete_inventory_item(self):
        response = self.client.delete("/inventory/1")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(
            data["message"],
            "Inventory item deleted successfully"
        )
        
    def test_delete_inventory_item_not_found(self):
        response = self.client.delete("/inventory/999")
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"],"Inventory item not found")
        
if __name__ == "__main__":
    unittest.main()