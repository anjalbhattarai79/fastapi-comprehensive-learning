from .database import client, session   
from app import models, schemas

    
def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "hello world"
    
def test_create_user(client):
    res = client.post("/users", json={"email": "test@125.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@125.com"
    assert res.status_code == 201

