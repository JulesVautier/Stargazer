from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    _password = Column(String(120))

    def __init__(self, email=None):
        self.name = email

    def __repr__(self):
        return "<User %r>" % (self.name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = pwd_context.hash(plaintext)

    def verify_password(self, plaintext, hashed_password):
        return pwd_context.verify(plaintext, hashed_password)
