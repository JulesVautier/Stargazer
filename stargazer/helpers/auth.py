from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from stargazer.crud.user import get_user
from stargazer.db.database import get_db
from stargazer.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:  # TODO add jwt to code/decode the token
        # payload = jwt.decode(
        #     token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        # )
        # token_data = schemas.TokenPayload(**payload)
        assert token
    # except (jwt.JWTError, ValidationError):
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = get_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
