from fastapi import FastAPI

from stargazer.api import api_router
from stargazer.db.database import get_db
from stargazer.scripts.create_super_user import create_super_user


def populate_db():
    db = next(get_db())
    create_super_user(db)


def create_app():
    app = FastAPI()

    app.include_router(
        api_router,
    )

    populate_db()
    return app


app = create_app()
