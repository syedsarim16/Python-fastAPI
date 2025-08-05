from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db_connection, Base
import pytest
from urllib.parse import quote_plus  # 👈 Import this

# Encode the password safely
encoded_password = quote_plus(settings.database_password)

# Use test DB with encoded password
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{encoded_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db_connection():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db_connection] = override_get_db_connection
    yield TestClient(app)