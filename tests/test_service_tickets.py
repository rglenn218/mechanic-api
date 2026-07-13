import unittest
from datetime import date

from config import TestingConfig
from application import create_app
from application.extensions import db
from application.models import Customer, Service, Mechanic, Inventory

class ServiceTicketTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            customer = Customer(
                name="Test Customer",
                email="customer@example.com",
                phone="5551234567",
                password="password123"
            )
            
            mechanic_one = Mechanic(
                name="Mechanic One",
                email="mechanic1@example.com",
                password="password123",
                phone="5551111111",
                salary=75000
            )
            
            mechanic_two = Mechanic(
                name="Mechanic Two",
                email="mechanic2@example.com",
                password="password123",
                phone="5552222222",
                salary=80000
            )
            
            part = Inventory(
                name="Brake Pads",
                price=89.99
            )
            
            db.session.add_all([
                customer,
                mechanic_one,
                mechanic_two,
                part
            ])
            
            db.session.commit()
            
            service_ticket = Service(
                VIN="123456789ABCDEFG",
                service_date=date(2026, 7, 6),
                service_desc="Oil change and brake inspection",
                customer_id=customer.id
            )
            
            service_ticket.mechanics.append(mechanic_one)
            
            db.session.add(service_ticket)
            db.session.commit()
            
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
    def test_create_service_ticket(self):
        response = self.client.post(
            "/service-tickets/",
            json={
            "VIN": "ABCDEFG123456789",
            "service_date": "2026-07-10",
            "service_desc": "Replace tires",
            "customer_id": 1
            }
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = response.get_json()
        
        self.assertIsNotNone(data["id"])
        self.assertEqual(data["VIN"], "ABCDEFG123456789")
        self.assertEqual(data["service_desc"], "Replace tires")
        self.assertEqual(data["customer_id"], 1)
        
    def test_create_service_ticket_customer_not_found(self):
        response = self.client.post(
            "/service-tickets/",
            json={
                "VIN": "ABCDEFG123456789",
                "service_date": "2026-07-10",
                "service_desc": "Replace tires",
                "customer_id": 999
            }
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Customer not found")
        
    def test_get_all_service_tickets(self):
        response = self.client.get("/service-tickets/")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["service_desc"],
            "Oil change and brake inspection"
        )
        
    def test_get_service_ticket_by_id(self):
        response = self.client.get("/service-tickets/1")
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["VIN"], "123456789ABCDEFG")
        self.assertEqual(data["customer_id"], 1)
        
    def test_get_service_ticket_not_found(self):
        response = self.client.get("/service-tickets/999")
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Service ticket not found")
        
    def test_assign_mechanic_to_service_ticket(self):
        response = self.client.put(
            "/service-tickets/1/assign-mechanic/2"
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(
            data["message"],
            "Mechanic assigned successfully"
        )
        
        with self.app.app_context():
            ticket = db.session.get(Service, 1)
            
            self.assertEqual(len(ticket.mechanics), 2)
            self.assertIn(2, [mechanic.id for mechanic in ticket.mechanics])
            
    def test_assign_mechanic_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/999/assign-mechanic/1"
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Service ticket not found")
        
    def test_assign_mechanic_not_found(self):
        response = self.client.put(
            "/service-tickets/1/assign-mechanic/999"
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Mechanic not found")
        
    def test_remove_mechanic_from_service_ticket(self):
        response = self.client.put(
            "/service-tickets/1/remove-mechanic/1"
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(
            data["message"],
            "Mechanic removed successfully"
        )
        
        with self.app.app_context():
            ticket = db.session.get(Service, 1)
            
            self.assertEqual(len(ticket.mechanics), 0)
            
    def test_edit_service_ticket_mechanics(self):
        response = self.client.put(
            "/service-tickets/1/edit",
            json={
                "add_ids": [2],
                "remove_ids": [1]
            }
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(
            data["message"],
            "Service ticket mechanics updated successfully"
        )
        
        with self.app.app_context():
            ticket = db.session.get(Service, 1)
            mechanic_ids = [
                mechanic.id for mechanic in ticket.mechanics
            ]
            
            self.assertNotIn(1, mechanic_ids)
            self.assertIn(2, mechanic_ids)
            
    def test_edit_service_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/999/edit",
            json={
                "add_ids": [2],
                "remove_ids": [1]
            }
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Service ticket not found")
        
    def test_add_part_to_service_ticket(self):
        response = self.client.put(
            "/service-tickets/1/add-part/1"
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        
        self.assertEqual(
            data["message"],
            "Part added to service ticket successfully"
        )
        
        with self.app.app_context():
            ticket = db.session.get(Service, 1)
            
            self.assertEqual(len(ticket.parts), 1)
            self.assertEqual(ticket.parts[0].name, "Brake Pads")
            
    def test_add_part_ticket_not_found(self):
        response = self.client.put(
            "/service-tickets/999/add-part/1"
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Service ticket not found")
        
    def test_add_part_not_found(self):
        response = self.client.put(
            "/service-tickets/1/add-part/999"
        )
        
        self.assertEqual(response.status_code, 404)
        
        data = response.get_json()
        
        self.assertEqual(data["error"], "Inventory item not found")
        
if __name__ == "__main__":
    unittest.main()