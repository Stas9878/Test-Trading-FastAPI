import fastapi_users
from fastapi_users import FastAPIUsers
from typing import List
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.manager import get_user_manager
from auth.database import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title='Trading App'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)