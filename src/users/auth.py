from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Request, Response

from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Session, select

from src.database import engine
from src.users.models import User
from src.users.schemas import UserInSchema

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user: User = session.exec(statement).one_or_none()
        return user


def authenticate_user(username: str, password: str):
    """Аутентифицирует пользователя."""
    user = get_user(username=username)
    if user is None:
        return {"message": "user not found"}
    if user and verify_password(password, user.hashed_password):
        return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return access_token


async def get_current_user(
    access_token: str = Depends(get_access_token),
) -> User | None:
    """Позволяет получить текущего пользователя."""
    try:

        payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    username: str = payload.get("sub")
    expire = payload.get("exp")
    if expire < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user: User | None = get_user(username)
    return user

UserDep = Annotated[User, Depends(get_current_user)]


def login(response: Response, user_data: UserInSchema):
    user = authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # httponly=True important for safety!!!
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return access_token
