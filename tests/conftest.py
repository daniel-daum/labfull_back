from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings
from src.database.database import Base
from fastapi.testclient import TestClient
from src.database.database import get_db
from src.main import app
from src.utilities import oauth2
import pytest


engine = create_engine(settings.DBSTR_TEST)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def create_user_fixture(client):
    """Creates a user in the test database"""
    user_data = {"first_name": "obi-wan", "last_name": "kenobi",
                 "email": "obi-wan@wustl.edu", "password": "password"}

    res = client.post("/api/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data['password']

    return new_user


@pytest.fixture
def token(create_user_fixture):
    return oauth2.create_access_token(data={"user_id": create_user_fixture['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
