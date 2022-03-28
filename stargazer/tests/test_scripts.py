from stargazer.models.user import User
from stargazer.scripts.create_super_user import create_super_user


def test_create_super_user(mocked_function_db):
    create_super_user(mocked_function_db)
    assert mocked_function_db.query(User).filter(User.username == "admin").first()
