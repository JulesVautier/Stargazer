from sqlalchemy.orm import Session

from stargazer.crud.user import create_user
from stargazer.db.database import get_db

users = [
    {
        "username": "admin",
        "password": "admin",
    }
]


def create_super_user(db: Session):
    for user in users:
        create_user(db, user)
    db.commit()


if __name__ == "__main__":
    db = next(get_db())
    create_super_user(db)
