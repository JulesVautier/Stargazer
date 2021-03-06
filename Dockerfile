FROM python:3.9

WORKDIR /app

RUN pip install poetry

COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry install --no-interaction --no-dev

COPY ./ /app/

CMD ["poetry", "run", "uvicorn", "stargazer.app:create_app", "--reload", "--host", "0.0.0.0", "--port", "80"]
