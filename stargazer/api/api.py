import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from stargazer import models
from stargazer.db.database import engine
from stargazer.helpers.auth import fake_users_db, UserInDB, fake_hash_password, get_current_active_user
from stargazer.helpers.github import GithubAPI
from stargazer.models.user import User

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/repos/{user}/{repo}/starneighbours")
async def get_starneighbours(
    user: str, repo: str, current_user: User = Depends(get_current_active_user)
):
    access_token = os.getenv("ACCESS_TOKEN")
    response = GithubAPI(access_token).get_neighbour_repositories(user, repo)
    return response
