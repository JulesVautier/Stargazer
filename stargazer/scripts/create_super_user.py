from stargazer.crud.user import create_user
from stargazer.db.database import get_db

users = [
    {
        "email": "admin",
        "password": "admin",
    }
]


def create_super_user():
    db = next(get_db())
    for user in users:
        create_user(db, user)
    db.commit()


if __name__ == "__main__":
    create_super_user()
