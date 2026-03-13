'''test client work similar to postman. It is like request library but for testing purpose.'''
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import models, schemas
from app.config import settings
from sqlalchemy.engine import create_engine
from app.database import get_db, Base
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test" # postgresql://<username>:<password>@<ip-address/hostname>/<database-name>
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    models.Base.metadata.drop_all(bind=engine) # clear earlier data if exist first, now latest test-data will be stored.
    models.Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):   
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db        
    yield TestClient(app)
        
  