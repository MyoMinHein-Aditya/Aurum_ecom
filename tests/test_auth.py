def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@aurum.com",
        "password": "supersecretpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@aurum.com"
    assert "id" in data

def test_login_user(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "test@aurum.com",
        "password": "supersecretpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
