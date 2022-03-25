FROM python:3.9

WORKDIR /stargazer

RUN pip install poetry

COPY poetry.lock /stargazer
COPY pyproject.toml /stargazer

RUN poetry install --no-interaction --no-ansi --no-dev

COPY . /stargazer

CMD ["poetry", "run", "uvicorn", "asgi:create_app", "--reload", "--host", "0.0.0.0", "--port", "80"]
