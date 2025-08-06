import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
import app.database as database
from app.database import Base
from app import models
from app.oauth2 import create_access_token

# Test DB connection string

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Engine and session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DB session fixture
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test client fixture with DB override
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[database.get_db_connection] = override_get_db
    yield TestClient(app)


# User creation fixture
@pytest.fixture
def test_user(client):
    user_data = {"email": "sarim@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    user = res.json()
    user['password'] = user_data['password']
    return user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "sarim16@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    user = res.json()
    user['password'] = user_data['password']
    return user


# Token fixture
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


# Authorized client fixture
@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


# Posts fixture
@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}
    ]

    posts = [models.Post(**post) for post in posts_data]
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()
