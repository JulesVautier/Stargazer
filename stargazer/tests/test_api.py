import pytest


def test_post_token_ok(client, populate_admin_user):
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin", "grant_type": "password"},
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "username, password",
    [("admin", "badpassword"), ("badusername", "admin")],
)
def test_post_token_ko(client, populate_admin_user, username, password):
    response = client.post(
        "/token",
        data={"username": username, "password": password},
    )
    assert response.status_code == 401


def test_auth_fail(client):
    response = client.get(
        "/repos/user/repo/starneighbours", headers={"Authorization": "Bearer badtoken"}
    )
    assert response.status_code == 401


def test_get_starneighbours(monkeypatch, client):
    def mocker_fct(self, user, repo):
        return {"repo": ["user"]}

    monkeypatch.setattr(
        "stargazer.helpers.github.GithubAPI.get_neighbour_repositories", mocker_fct
    )
    response = client.get(
        "/repos/user/repo/starneighbours", headers={"Authorization": "Bearer admin"}
    )
    assert response.status_code == 200
    assert response.json() == {"repo": ["user"]}
