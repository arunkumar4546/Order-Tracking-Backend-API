# 📦 Order Tracking Backend API

A scalable backend system built using **FastAPI** to manage users, orders, and order history with authentication and role-based access.

---

## 🚀 Project Overview

This project simulates a real-world **order tracking system**, where users can place orders and track their status, while admins can monitor and manage all orders.

It follows a clean backend architecture with modular structure and RESTful APIs.

---

## 🧠 Key Features

- 🔐 JWT Authentication (Login & Secure APIs)
- 👤 User Management
- 📦 Order Creation & Tracking
- 📜 Order History Tracking (status updates)
- 🛡️ Role-Based Access (Admin/User)
- 🗄️ Database Integration using SQLAlchemy
- ⚙️ Modular Project Structure

---

## 🏗️ Tech Stack

- **Backend:** FastAPI  
- **Database:** SQLite / PostgreSQL  
- **ORM:** SQLAlchemy  
- **Authentication:** JWT  
- **Validation:** Pydantic  
- **Server:** Uvicorn  

---

## 📂 Project Structure
app/
│
├── api/                # Route handlers
├── core/               # Config, security
├── models/             # Database models
├── schema/             # Pydantic schemas
│
├── main.py             # Entry point
├── db.py               # Database connection
│
.env                    # Environment variables
requirements.txt        # Dependencies

---


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/order-tracking-api.git
cd order-tracking-api


### 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Setup Environment Variables

Create a .env file:

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL="yoursqlserver"

### 5️⃣ Run the Server
uvicorn app.main:app --reload

---

📖 API Documentation
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc

---

🔑 API Endpoints (Sample)
Auth
POST /login → Login user
Orders
POST /orders → Create order
GET /orders → Get user orders
GET /allorders → Admin access
Order History
Tracks order status updates

---

🔄 Workflow
User logs in and receives JWT token
User creates an order
Order is stored with status PLACED
Order history updates (SHIPPED, DELIVERED)
Admin can view all orders

---

🧪 Example Use Cases
E-commerce backend
Delivery tracking system
Inventory/order management

---

📈 Future Improvements
🐳 Docker Support
⚡ Redis Caching
🧪 Unit Testing

---

👨‍💻 Author

ARUNKUMAR A
Backend Developer (Python | FastAPI)
