from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from stargazer import models
from stargazer.db.database import engine, get_db
from stargazer.helpers.auth import get_current_user
from stargazer.helpers.github import GithubAPI
from stargazer.models.user import User
from stargazer.schemas.startneighbor import StarneighborSchema

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

fake_users_db = None


@router.post("/token")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/repos/{user}/{repo}/starneighbours", response_model=List[StarneighborSchema])
async def get_starneighbours(user: str, repo: str, current_user: User = Depends(get_current_user)):
    return GithubAPI().get_neighbour_repositories(user, repo)
