from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings
from src.database.database import Base
from fastapi.testclient import TestClient
from src.database.database import get_db
from src.main import app
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
