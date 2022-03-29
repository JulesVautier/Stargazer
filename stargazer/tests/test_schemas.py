from stargazer.schemas.startneighbor import StarneighborSchema


def test_starneighbours_schema():
    data = {
        "repo": "repoA",
        "stargazers": ["user1", "user2"],
    }

    starneighbor = StarneighborSchema(**data)

    assert starneighbor.repo == data["repo"]
    assert starneighbor.stargazers == data["stargazers"]
