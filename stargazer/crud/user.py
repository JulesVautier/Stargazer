from sqlalchemy.orm import Session

from stargazer.models.user import User


def create_user(db: Session, user):
    db_user = User(username=user["username"])
    db_user.set_password(user["password"])
    db.add(db_user)
    db.flush()
    return db_user


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).one_or_none()
    return user
