from datetime import datetime
from src.database import schemas, models
from jose import jwt
from src.settings import settings


def test_create_user(client, session):

    res = client.post("/api/users/", json={"first_name": "anakin",
                      "last_name": "skywalker", "email": "anakin@wustl.edu", "password": "password"})

    new_user = schemas.User(**res.json())

    assert res.status_code == 201
    assert new_user.first_name == "anakin"
    assert new_user.last_name == "skywalker"
    assert new_user.email == "anakin@wustl.edu"
    assert new_user.id == 1
    assert type(new_user.created_at) == datetime

    session.query(models.User).delete()
    session.commit()




def test_email_suffix(client):
    res = client.post("/api/users/", json={"first_name": "ashoka",
                      "last_name": "tano", "email": "ashoka@outlook.com", "password": "password"})

    assert res.status_code == 400
    assert res.json().get('detail') == "You must register with a @wustl.edu email address."


def test_email_duplicate(client, create_user_fixture):
    client.post("/api/users/", json={"first_name": "qui-gon",
                      "last_name": "jinn", "email": "qui-gon@wustl.edu", "password": "password"})

    res = client.post("/api/users/", json={"first_name": "qui-gon",
                    "last_name": "jinn", "email": "qui-gon@wustl.edu", "password": "password"})

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


def test_get_user_by_id(authorized_client, create_user_fixture):
    res = authorized_client.get("/api/users/1")

    user = schemas.User(**res.json())

    assert res.status_code == 200
    assert create_user_fixture['id'] == user.id
    assert create_user_fixture['first_name'] == user.first_name
    assert create_user_fixture['last_name'] == user.last_name
    assert create_user_fixture['email'] == user.email
    assert type(user.created_at) == datetime


def test_get_user_by_id_failure(authorized_client,create_user_fixture):
    res = authorized_client.get("/api/users/2")

    assert res.status_code == 404
    assert res.json().get('detail') == "User with id: 2 was not found"
     
 
def test_get_all_users(authorized_client):
    res = authorized_client.get("/api/users/")

    print(res.json())
    assert res.status_code == 200




