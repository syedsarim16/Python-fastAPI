from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db_connection,Base

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username
                                          }:{settings.database_password
                                             }@{settings.database_hostname
                                                }:{settings.database_port
                                                   }/{settings.database_name
                                                      }_test'


engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) 

def override_get_db_connection():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_connection]=override_get_db_connection

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert(res.json().get('message'))=='Hello World'
    assert(res.status_code)==200

def test_create_user():
    res = client.post("/users/", json={"email": "safwan@gmail.com", "password": "safwan123"})
    new_user=schemas.UserResponse(**res.json())
    assert new_user.email== "safwan@gmail.com"
    assert res.status_code == 201