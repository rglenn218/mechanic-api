# Mechanic Shop API

A RESTful API built with Flask, SQLAlchemy, Marshmallow and MySQL for managing customers, mechanics, and vehicle service tickets. This project demonstrates CRUD operations, relational database modeling, Marshmallow serialization and the Flask Application Factory Pattern.

---

## Version 4 Update

The final version of this project completes the transition from a locally developed REST API to a production-ready application with automated deployment.

Version 4 focuses on continuous integration, continuous deployment (CI/CD), cloud hosting, and production configuration.

---

### New Features

- Live deployment of the API using Render
- Production PostgreSQL database hosted on Render
- Separate Development, Testing and Production configurations
- Gunicorn WSGI server for production deployment
- GitHub Actions CI/CD pipeline
- Automatic build verification on every push to the `main` branch
- Automated execution of all 42 unit tests before deployment
- Automatic deployment to Render using the Render API
- Production environment variables managed securely through GitHub Secrets and Render Environment Variables
- Swagger documentation updated for the live production API over HTTPS

--- 

### Continuous Integration & Continuous Deployment

Every push to the `main` branch now triggers an automated GitHub Actions workflow that:

1. Checks out the repository
2. Sets up the Python environment
3. Installs project dependencies
4. Verifies the application builds successfully
5. Executes all 42 automated unit tests
6. Deploys the application to Render only after all tests pass

This ensures only verified, tested code reaches the production environment.

---

### Production Deployment

The application is now deployed using:

- Render Web Service
- Render PostgreSQL Database
- Gunicorn
- GitHub Actions
- Render API

Production credentials are managed securely through environment variables and are never committed to source control.

---

### Live API

The deployed API includes:

- Interactive Swagger documentation
- Production PostgreSQL database
- HTTPS endpoints
- Automatic deployments from GitHub

---

### Additional Technologies

The following technologies were added during Version 4:

- Render
- PostgreSQL
- Gunicorn
- GitHub Actions
- psycopg2-binary

## Version 3 Update

This project has been expanded into a production-style REST API with comprehensive API documentation and automated testing.

Version 3 focuses on production readiness by adding comprehensive API documentation and automated testing to improve maintainability, reliability, and developer experience.

---

### New Features

- Interactive API documentation using Flask-Swagger and Flask-Swagger-UI
- Complete Swagger documentation for every endpoint
- Request payload definitions and reusable response schemas
- Bearer Token authentication documented within Swagger
- Comprehensive automated testing suite using Python's built-in `unittest`
- Individual test modules for Customers, Mechanics, Service Tickets, and Inventory
- Positive and negative test coverage for every API resource
- Dedicated testing configuration using a separate MySQL test database
- Improved project structure supporting production and testing environments

---

### Testing

The project now includes **42 automated unit tests** covering:

- Customer endpoints
- Mechanic endpoints
- Service Ticket endpoints
- Inventory endpoints
- Authentication
- Authorization
- CRUD operations
- Relationship management
- Error handling
- Protected routes

Run the complete test suite with:

```bash
python -m unittest discover tests
```

---

### API Documentation

Interactive Swagger documentation is available after starting the server:

```
http://127.0.0.1:5001/api/docs
```

The documentation includes:

- Every API endpoint
- Request payload examples
- Response examples
- Authentication requirements
- Reusable schema definitions
- Interactive endpoint explorer

---

### Additional Technologies

The following libraries were added during Version 3:

- Flask-Swagger
- Flask-Swagger-UI
- unittest

---

## Version 2 Update

This project has been significantly expanded beyond the original CRUD API to demonstrate more advanced backend development concepts using Flask and SQLAlchemy.

---

### New Features

- JWT authentication for Customers and Mechanics using `python-jose`
- Protected API endpoints with Bearer Token authorization
- Customer and Mechanic login endpoints
- Customer-specific endpoint to retrieve only their own service tickets
- Inventory resource with full CRUD operations
- Many-to-many relationship between Inventory and Service Tickets
- Route to add inventory parts to existing service tickets
- Advanced service ticket editing to add and remove multiple mechanics in a single request
- Mechanic leaderboard endpoint returning mechanics ordered by number of completed service tickets
- Pagination for customer listings
- Flask-Limiter rate limiting for authentication routes
- Flask-Caching implementation for frequently requested endpoints
- Environment variable support using `.env`
- MySQL credentials removed from source control
- Explanded Postman collection covering all endpoints, authentication, inventory management, pagination and advanced relationship routes

---

### Additional Technologies

The following libraries were added during Version 2:

- Flask-Limiter
- Flask-Caching
- python-jose
- python-dotenv

---

## New API Endpoints

### Authentication

POST | `/customers/login` | Customer login
POST | `/mechanics/login` | Mechanic login
GET | `/customers/my-tickets/` | Returns authenticated customer's service tickets

### Inventory

POST | `/inventory/` | Create inventory part
GET | `/inventory/` | Get all inventory parts
GET | `/inventory/<id>` | Get inventory part by ID
PUT | `/inventory/<id>` | Update inventory part
DELETE | `/inventory/<id>` | Delete inventory part

### Advanced Endpoints

PUT | `/service-tickets/<ticket_id>/edit` | Edit service ticket mechanics
PUT | `/service-tickets/<ticket_id>/add-part/<part_id>` | Add part to service ticket
GET | `/mechanics/most-tickets` | Get mechanics by most tickets

---

## Authentication

Protected routes require a Bearer Token obtained from the appropriate login endpoint.

Example request header:

```text
Authorization: Bearer <JWT_TOKEN>
```

Customer tokens authorize customer-specific routes, while mechanic tokens authorize mechanic-specific routes.

---

## Features

- Customer CRUD operations
- Mechanic CRUD operations
- Inventory CRUD operations
- JWT Authentication
- Protected routes with Bearer Tokens
- Customer-specific service ticket retrieval
- Create and manage service tickets
- Assign mechanics to service tickets
- Remove mechanics from service tickets
- Add inventory parts to service tickets
- Edit mechanics assigned to service tickets
- Mechanic ranking endpoint
- Pagination
- Rate limiting
- Response caching
- Marshmallow serialization and validation
- Blueprint architecture using the Application Factory Pattern
- MySQL database integration
- Interactive Swagger API documentation
- Automated unit testing (42 tests)
- Separate testing configuration and database

---

## Technologies Used

- Python 3
- Flask
- Flask SQLAlchemy
- SQLAlchemy
- Flask Marshmallow
- Marshmallow
- MySQL (Development & Testing)
- PostgreSQL (Production)
- MySQL Connector/Python
- psycopg2-binary
- Gunicorn
- GitHub Actions
- Render
- Flask-Limiter
- Flask-Caching
- python-jose
- Flask-Swagger
- Flask-Swagger-UI
- unittest

---

## Project Structure

```text
mechanic-api/
│
├── application/
│   ├── blueprints/
│   │   ├── customer/
│   │   ├── mechanic/
│   │   ├── service_ticket/
│   │   └── inventory/
│   ├── static/
│   │   └── swagger.json
│   ├── extensions.py
│   ├── models.py
│   └── utils.py
│
├── tests/
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_service_tickets.py
│   └── test_inventory.py
│
├── flask_app.py
├── config.py
├── requirements.txt
├── mechanic-api-postman-collection.json
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
- One Service Ticket can use many Inventory Parts
- One Inventory Part can be used on many Service Tickets

---

## Author

Rachel Glenn