from sqlalchemy.orm import Session

from stargazer.crud.user import create_user
from stargazer.db.database import get_db
from stargazer.models.user import User

super_user = {
    "username": "admin",
    "password": "admin",
}


def create_super_user(db: Session):
    admin = db.query(User).filter(User.username == "admin").one_or_none()
    if not admin:
        create_user(db, super_user)
    db.commit()


if __name__ == "__main__":
    db = next(get_db())
    create_super_user(db)
