from datetime import datetime
from src.database import schemas
from jose import jwt
from src.settings import settings

def test_create_user(client):

    res = client.post("/api/users/", json={"first_name": "obi-wan",
                      "last_name": "kenobi", "email": "obi-wan@wustl.edu", "password": "password"})

    new_user = schemas.User(**res.json())

    assert res.status_code == 201
    assert new_user.first_name == "obi-wan"
    assert new_user.last_name == "kenobi"
    assert new_user.email == "obi-wan@wustl.edu"
    assert new_user.id == 1
    assert type(new_user.created_at) == datetime


def test_email_suffix(client):
    res = client.post("/api/users/", json={"first_name": "obi-wan",
                      "last_name": "kenobi", "email": "obi-wan@outlook.com", "password": "password"})

    assert res.status_code == 400
    assert res.json().get('detail') == "You must register with a @wustl.edu email address."


def test_email_duplicate(client, create_user_fixture):
    res = client.post("/api/users/", json={"first_name": "obi-wan",
                      "last_name": "kenobi", "email": "obi-wan@wustl.edu", "password": "password"})

    assert res.status_code == 400
    assert res.json().get('detail') == "Email already registered"


def test_user_login(client, create_user_fixture):

    res = client.post("/api/auth/login",
                      data={"username": create_user_fixture['email'], "password": create_user_fixture['password']})

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.KEY, algorithms=[settings.ALGO])

    id = payload.get("user_id")
    
    assert res.status_code == 200
    assert id == create_user_fixture['id']
    assert login_res.token_type == "bearer"
   
def test_user_login_password_failure(client, create_user_fixture):

    res = client.post("/api/auth/login",
                      data={"username": create_user_fixture['email'], "password":"incorrectPassword"})
    
    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid Credentials" 
    
def test_user_login_email_failure(client, create_user_fixture):

    res = client.post("/api/auth/login",
                      data={"username": "incorrect@email.com", "password":create_user_fixture['password']})
    
    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid Credentials"


    
def test_get_user_by_id(authorized_client):
    res = authorized_client.get("/api/users/")
    print(res.json())

