from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    _password = Column(String(120))

    def __init__(self, username=None):
        self.username = username

    def __repr__(self):
        return "<User %r>" % (self.username)

    @hybrid_property
    def password(self):
        return self._password

    def set_password(self, plaintext):
        self._password = pwd_context.hash(plaintext)

    def verify_password(self, plaintext):
        return pwd_context.verify(plaintext, self._password)
