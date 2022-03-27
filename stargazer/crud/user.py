from sqlalchemy.orm import Session

from stargazer.models.user import User


def create_user(db: Session, user):
    """
    Create user record
    """
    db_user = User(email=user["email"])
    db_user.set_password(user["password"])
    db.add(db_user)
    db.flush()
    return db_user
