# Stargazer

This repo is the answer of this [test](https://mergify.notion.site/Stargazer-4cf5427e34a542f0aee4e829bb6d9035).

The project uses two container:
1. A FastApi docker containing the API
2. A PostgreSQL docker containing the Database, where is stored the admin user.

I could have [auto-generated](https://github.com/tiangolo/full-stack-fastapi-postgresql) this project but this test would have been way less interresting, in addition it allowed me to review the basics and how to set up a FastAPI dockerized project.  

## Getting started

First, you need to generate a Github Token with rights to read repos and users in order to allow the app to perform request on Github:
https://github.com/settings/tokens/new

```bash
docker-compose build
env ACCESS_TOKEN=<your_access_token> docker-compose up
```

Then browse: http://localhost/docs

This app requires authentification.
You can login using the `Authorize` button on the top right of the page.

```
login: admin
password: admin
```

After that, you will be able to use the Get starneighbours endpoint to get nieghbhours of a given Github repository.

## Testing

```
poetry install
poetry shell
pytest .
```

## Possible improvements (not ordered)

* Use JWToken to encode/decode authentication tokens
* Use schemas to validate/serialize data and have a strong typing in the code.
* Split the GithubAPI.get_neighbour_repositories function in several little function like doing specific things like get_repo, get_user, get_starred_repos_from_user, in order to use them later in futures endpoints.
* Use gunicorn to create multiple worker for the API in order to handle more requests simultaneously.
* Use migrations with Alembic to manage database models
* Use Github Oauth2 in order to authenticate users and use their own Github Token
* Use Postgres database for tests too, instead of SQLite. (It was faster to setup)
