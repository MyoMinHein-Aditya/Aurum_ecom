def test_checkout_empty_cart(client):
    # Register and login to get token
    client.post("/api/v1/auth/register", json={"email": "order@aurum.com", "password": "supersecretpassword"})
    login_res = client.post("/api/v1/auth/login", json={"email": "order@aurum.com", "password": "supersecretpassword"})
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to checkout with empty cart
    response = client.post("/api/v1/orders/checkout", json={"address": "123 Luxury Ave, Beverly Hills, CA 90210"}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Cart is empty"
