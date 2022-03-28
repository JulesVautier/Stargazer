from stargazer.crud.user import create_user
from stargazer.models.user import User


def test_create_user(mocked_session_db):
    user = {
        "username": "test",
        "password": "test",
    }
    create_user(mocked_session_db, user)
    mocked_session_db.commit()

    user = mocked_session_db.query(User).filter(User.username == "test").first()
    assert user
    assert user.verify_password("test")
