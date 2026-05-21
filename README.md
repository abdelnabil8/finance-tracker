
# Personal Finance Tracker# ⬡ Personal Finance Tracker

A full-stack web application to track personal income and expenses, built from scratch with a futuristic dark/green UI.

> 🔴 **Live Demo:** [https://finance-tracker-hyv7.onrender.com](https://finance-tracker-hyv7.onrender.com)

---

## Features

- 🔐 **JWT Authentication** — register, login, logout with secure token-based auth
- 💰 **Transaction Management** — add and delete income/expense transactions
- 📊 **Live Summary** — real-time total income, expenses and balance cards
- 🍩 **Expense Chart** — doughnut chart showing expenses by category (Chart.js)
- 🔍 **Filters** — filter transactions by type and category
- 🗄️ **Persistent Storage** — PostgreSQL database, data survives restarts
- 🐳 **Dockerized** — runs fully in Docker containers
- ✅ **Tested** — 13 pytest tests covering all endpoints and edge cases
- 🚀 **CI/CD** — GitHub Actions pipeline runs tests on every push to main

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose), bcrypt |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| DevOps | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Hosting | Render.com |

---

## Getting Started Locally

### Prerequisites
- Docker Desktop installed
- Git

### Run the app
```bash
# Clone the repo
git clone https://github.com/abdelnabil8/finance-tracker
cd finance-tracker

# Create .env file
echo "DATABASE_URL=postgresql://user:password@db:5432/financedb" > .env
echo "SECRET_KEY=yoursecretkey" >> .env

# Start with Docker
docker-compose up --build
```

Open **http://localhost:8000**

### Run tests
```bash
# Activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/auth/register | Register a new user | ❌ |
| POST | /api/auth/login | Login and get JWT token | ❌ |
| GET | /api/transactions/ | Get all transactions | ✅ |
| POST | /api/transactions/ | Add a transaction | ✅ |
| DELETE | /api/transactions/{id} | Delete a transaction | ✅ |

---

## Project Structure

```
finance-tracker/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── models.py        # SQLAlchemy & Pydantic models
│   ├── routes.py        # Transaction endpoints
│   ├── routes_auth.py   # Auth endpoints
│   ├── auth.py          # JWT logic
│   └── database.py      # Database connection
├── frontend/
│   ├── index.html       # Main HTML page
│   ├── style.css        # Dark/green futuristic theme
│   └── app.js           # Frontend JavaScript
├── tests/
│   ├── conftest.py      # Test configuration
│   └── test_transactions.py  # All tests
├── .github/workflows/
│   └── deploy.yml       # GitHub Actions CI/CD
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## CI/CD Pipeline

Every push to `main` triggers GitHub Actions which:
1. Sets up Python 3.11
2. Installs all dependencies
3. Runs all 13 pytest tests
4. If tests pass → Render auto-deploys the new version

---

## Author

**Abdellah Nabil**
CS Student @ Hochschule Darmstadt
[GitHub](https://github.com/abdelnabil8) · [LinkedIn](https://www.linkedin.com/in/abdellah-nabil-9b9ba4328/)
