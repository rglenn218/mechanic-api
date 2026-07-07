# Mechanic Shop API

A RESTful API built with Flask, SQLAlchemy, Marshmallow and MySQL for managing customers, mechanics, and vehicle service tickets. This project demonstrates CRUD operations, relational database modeling, Marshmallow serialization and the Flask Application Factory Pattern.

---

## Features

- Customer CRUD operations
- Mechanic CRUD operations
- Create and manage service tickets
- Assign mechanics to service tickets
- Remove mechanics from service tickets
- Many-to-many relationship between mechanics and service tickets
- Marshmallow serialization and validation
- Blueprint architecture using the Application Factory Pattern
- MySQL database integration

---

## Technologies Used

- Python 3
- Flask
- Flask SQLAlchemy
- SQLAlchemy
- Flask Marshmallow
- Marshmallow
- MySQL
- MySQL Connector/Python
- python-dotenv

---

## Project Structure

```text
mechanic-api/
│
├── application/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── blueprints/
│       ├── customer/
│       ├── mechanic/
│       └── service_ticket/
│
├── app.py
├── config.py
├── .env.example
├── Mechanic_Shop_API.postman_collection.json
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
```

Navigate into the project.

```bash
cd mechanic-api
```

Create and activate a virtual environment.

### macOS/Linux

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root using the provided `.env.example`.

Example:

```sh
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=mechanic_db
```

Create the MySQL database before running the application.

```sql
CREATE DATABASE mechanic_db;
```

---

## Running the Application

Start the Flask server.

```bash
python app.py
```

The API runs on:

```
http://127.0.0.1:5001
```

NOTE: Port 5000 is taken up by AirPlay on Mac devices. Therefore, Port 5001 is hardcoded as the specified port in this project.

---

## API Endpoints

### Customers

POST | `/customers/` | Create customer 
GET | `/customers/` | Get all customers 
GET | `/customers/<id>` | Get customer by ID 
PUT | `/customers/<id>` | Update customer 
DELETE | `/customers/<id>` | Delete customer 

---

### Mechanics

POST | `/mechanics/` | Create mechanic
GET | `/mechanics/` | Get all mechanics
GET | `/mechanics/<id>` | Get mechanic by ID
PUT | `/mechanics/<id>` | Update mechanic
DELETE | `/mechanics/<id>` | Delete mechanic

---

### Service Tickets

POST | `/service-tickets/` | Create service ticket
GET | `/service-tickets/` | Get all service tickets
GET | `/service-tickets/<id>` | Get service ticket by ID
PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign mechanic
PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove mechanic

---

## Testing

All endpoints were tested using Postman.

The exported Postman collection is included in this repository in the root folder:

```
mechanic-api-postman-collection.json
```

---

## Database Relationships

- One Customer can have many Service Tickets
- Each Service Ticket belongs to one Customer
- One Service Ticket can have many Mechanics
- One Mechanic can work on many Service Tickets

---

## Author

Rachel Glenn