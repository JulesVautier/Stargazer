from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from stargazer.app import app
from stargazer.db.database import Base, get_db
from stargazer.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def mocked_session_db() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def mocked_function_db() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def populate_admin_user(mocked_session_db):
    user = User(username="admin")
    user.set_password("admin")
    mocked_session_db.add(user)
    mocked_session_db.commit()


@pytest.fixture()
def github_token(monkeypatch):
    monkeypatch.setenv("ACCESS_TOKEN", "test_token")


@pytest.fixture()
def client(github_token, populate_admin_user):
    return TestClient(app)
