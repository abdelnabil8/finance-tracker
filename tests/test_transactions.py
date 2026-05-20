def test_create_transaction(client):
    response = client.post("/api/transactions/", json={
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

def test_get_transactions(client):
    response = client.get("/api/transactions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_transaction(client):
    # First create one
    create = client.post("/api/transactions/", json={
        "title": "Test",
        "amount": 10.0,
        "type": "income",
        "category": "Salary"
    })
    transaction_id = create.json()["id"]

    # Then delete it
    response = client.delete(f"/api/transactions/{transaction_id}")
    assert response.status_code == 200

def test_invalid_transaction(client):
    # Missing required fields
    response = client.post("/api/transactions/", json={
        "title": "No amount"
    })
    assert response.status_code == 422