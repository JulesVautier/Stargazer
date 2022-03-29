from typing import Generator

from stargazer.helpers.github import GithubAPI


class MockedResponse:
    def __init__(self, status_code, result):
        self.status_code = status_code
        self.result = result

    def json(self):
        return self.result


def test_github_api_get_neighbour_repositories(monkeypatch):
    """
    Simulates multiple consecutive calls the the Github API
    """

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
    assert res == [{"repo": "repo_test", "stargazers": ["user_1", "user_2"]}]
