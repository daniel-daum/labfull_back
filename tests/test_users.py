from datetime import datetime
from .database_testing import client, session
from src.database import schemas


def test_create_user(client):

    res = client.post("/api/users/", json={"first_name": "christie", "last_name": "crandall","email": "christie@outlook.com", "password": "password1"})

    new_user = schemas.User(**res.json())

    assert res.status_code == 201
    assert new_user.first_name == "christie"
    assert new_user.last_name == "crandall"
    assert new_user.email == "christie@outlook.com"
    assert new_user.id == 1
    assert type(new_user.created_at) is datetime

    
