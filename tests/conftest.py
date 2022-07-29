# import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings
from src.database.database import Base
from fastapi.testclient import TestClient
from src.database.database import get_db
from src.main import app
# from src.utilities import oauth2
# from src.database import models, schemas
import pytest


engine = create_engine(settings.DBSTR_TEST)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


# @pytest.fixture(scope="function")
# def create_user_fixture(client):
#     """Creates a user in the test database"""
#     user_data = {"first_name": "daniel", "last_name": "daum",
#                  "email": "daniel@wustl.edu", "password": "password"}

#     res = client.post("/api/users/", json=user_data)

#     new_user = res.json()
#     new_user["password"] = user_data['password']

#     return new_user


# @pytest.fixture(scope="function")
# def token(create_user_fixture):
#     return oauth2.create_access_token(data={"user_id": create_user_fixture['id']})


# @pytest.fixture(scope="function")
# def authorized_client(client, token):
#     client.headers = {
#         **client.headers,
#         "Authorization": f"Bearer {token}"
#     }

#     return client


# @pytest.fixture(scope="function")
# def create_multiple_users(authorized_client):

#     user_data = [{"first_name": "darth", "last_name": "revan", "email": "revan@wustl.edu", "password": "password"},
#              {"first_name": "darth", "last_name": "malak", "email": "malak@wustl.edu", "password": "password"},
#              {"first_name": "darth", "last_name": "valkorian", "email": "valkorian@wustl.edu", "password": "password"}]

#     res1 = authorized_client.post("/api/users/", json=user_data[0])
#     res2 = authorized_client.post("/api/users/", json=user_data[1])
#     res3 = authorized_client.post("/api/users/", json=user_data[2])

#     user1 = res1.json()
#     user2 = res2.json()
#     user3 = res3.json()

#     users = [user1,user2,user3]

#     return users


 
# @pytest.fixture(scope="function")
# def create_user_for_delete(authorized_client):

#     user_data = {"first_name":"kylo", "last_name":"ren", "email":"kyloe@wustl.edu", "password":"password"}

#     res = authorized_client.post("/api/users/", json=user_data)

#     user = res.json()

#     return user


# @pytest.fixture(scope="function")
# def create_supply_item(authorized_client):

#     supply = {"item_name":"starfruit","quantity":80, "date_ordered":"2022-06-07", "temp_sensitive":"no",  "users_id":1}

#     res = authorized_client.post("/api/supplies/", json=supply)

#     new_supply = schemas.Supply(**res.json())

#     return new_supply

# @pytest.fixture(scope="function")
# def create_multiple_supplies(authorized_client):

#     supplies = [{"item_name":"starfruit","quantity":80, "date_ordered":"2022-06-07", "temp_sensitive":"no",  "users_id":1},
#                  {"item_name":"toilet paper","quantity":30, "date_ordered":"2022-06-07", "temp_sensitive":"no",  "users_id":1},
#                  {"item_name":"chips","quantity":1, "date_ordered":"2022-06-07", "temp_sensitive":"no",  "users_id":1}]


#     res1 = authorized_client.post("/api/supplies/", json=supplies[0])
#     res2 = authorized_client.post("/api/supplies/", json=supplies[1])
#     res3 = authorized_client.post("/api/supplies/", json=supplies[2])

#     supply1 = res1.json()
#     supply2 = res2.json()
#     supply3 = res3.json()

#     supply_list = [supply1, supply2, supply3]

#     return supply_list









        

    

