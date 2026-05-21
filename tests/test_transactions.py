# --- Transaction Tests ---

def test_create_transaction(auth_client):
    response = auth_client.post("/api/transactions/", json={
        "title": "Grocery",
        "amount": 45.50,
        "type": "expense",
        "category": "Food"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Grocery"
    assert data["amount"] == 45.50
    assert data["type"] == "expense"

def test_get_transactions(auth_client):
    response = auth_client.get("/api/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_transaction(auth_client):
    create = auth_client.post("/api/transactions/", json={
        "title": "Test",
        "amount": 10.0,
        "type": "income",
        "category": "Salary"
    })
    transaction_id = create.json()["id"]
    response = auth_client.delete(f"/api/transactions/{transaction_id}")
    assert response.status_code == 200

def test_invalid_transaction(auth_client):
    response = auth_client.post("/api/transactions/", json={
        "title": "No amount"
    })
    assert response.status_code == 422

def test_unauthorized_access(client):
    response = client.get("/api/transactions/")
    assert response.status_code == 401

# --- Auth Tests ---

def test_register(client):
    response = client.post("/api/auth/register", json={
        "username": "newuser",
        "email": "new@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_register_duplicate_username(client):
    client.post("/api/auth/register", json={
        "username": "dupuser",
        "email": "dup@test.com",
        "password": "password123"
    })
    response = client.post("/api/auth/register", json={
        "username": "dupuser",
        "email": "dup2@test.com",
        "password": "password123"
    })
    assert response.status_code == 400

def test_login(client):
    client.post("/api/auth/register", json={
        "username": "loginuser",
        "email": "login@test.com",
        "password": "password123"
    })
    response = client.post("/api/auth/login", json={
        "username": "loginuser",
        "email": "",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "wrongpass",
        "email": "wrong@test.com",
        "password": "correctpass"
    })
    response = client.post("/api/auth/login", json={
        "username": "wrongpass",
        "email": "",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_filter_by_type(auth_client):
    auth_client.post("/api/transactions/", json={"title": "Salary", "amount": 2000.0, "type": "income", "category": "Salary"})
    auth_client.post("/api/transactions/", json={"title": "Food", "amount": 50.0, "type": "expense", "category": "Food"})
    
    response = auth_client.get("/api/transactions/?type=expense")
    assert response.status_code == 200
    assert all(t["type"] == "expense" for t in response.json())

def test_filter_by_category(auth_client):
    auth_client.post("/api/transactions/", json={"title": "Food", "amount": 50.0, "type": "expense", "category": "Food"})
    auth_client.post("/api/transactions/", json={"title": "Bus", "amount": 20.0, "type": "expense", "category": "Transport"})
    
    response = auth_client.get("/api/transactions/?category=Food")
    assert response.status_code == 200
    assert all(t["category"] == "Food" for t in response.json())

def test_delete_nonexistent(auth_client):
    response = auth_client.delete("/api/transactions/9999")
    assert response.status_code == 404

def test_invalid_token(client):
    client.headers.update({"Authorization": "Bearer faketoken"})
    response = client.get("/api/transactions/")
    assert response.status_code == 401