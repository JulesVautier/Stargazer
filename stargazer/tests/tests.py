from pprint import pprint
from typing import Generator

from requests import Response
from sqlalchemy.orm import Session

from stargazer.crud.user import create_user
from stargazer.helpers.github import GithubAPI
from stargazer.main import app
from stargazer.models.user import User
from stargazer.scripts.create_super_user import create_super_user


def test_create_user(db: Session):
    user = {
        "email": "test",
        "password": "test",
    }
    create_user(db, user)
    db.commit()

    user = db.query(User).filter(User.email == "test").first()
    assert user
    assert user.verify_password("test")


def test_create_super_user(db: Session):
    create_super_user()
    assert db.query(User).filter(User.email == "admin").first()


class MockedResponse:
    def __init__(self, status_code, result):
        self.status_code = status_code
        self.result = result

    def json(self):
        return self.result


def test_get_neighbour_repositories(monkeypatch):
    def _response_values() -> Generator:
        yield MockedResponse(200, {"stargazers_url": "stargazers_url"})
        yield MockedResponse(
            200,
            [
                {
                    "login": "user_1",
                    "starred_url": "https://api.github.com/users/user_1/starred{/owner}{/repo}",
                },
                {
                    "login": "user_2",
                    "starred_url": "https://api.github.com/users/user_2/starred{/owner}{/repo}",
                },
            ],
        )
        yield MockedResponse(200, [{"name": "repo_test"}])
        yield MockedResponse(200, [{"name": "repo_test"}])

    response_values = _response_values()

    def mocked_get(url, headers):
        return next(response_values)

    monkeypatch.setattr("stargazer.helpers.github.requests.get", mocked_get)

    g = GithubAPI("fake_token")
    res = g.get_neighbour_repositories("test_username", "test_repo")
    assert res == {"repo_test": {"user_2", "user_1"}}
