from app import models, schemas
from jose import jwt
from app.config import settings
import pytest

    
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "hello world"
    
def test_create_user(client):
    res = client.post("/users", json={"email": "test@125.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@125.com"
    assert res.status_code == 201



def test_login_user(client, test_user):
    res = client.post("auth/login", data={"username": test_user['email'], "password": test_user['password']})   
    login_res = schemas.Token(**res.json())
    
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    # print(payload)
    id= payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"    
    
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@125.com', 'password123', 403),
    ('test@125.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test@125.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("auth/login", data={"username": email, "password": password})   
    assert res.status_code == status_code
    
