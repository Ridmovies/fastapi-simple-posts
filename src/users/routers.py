from fastapi import APIRouter, HTTPException, status, Response
from sqlmodel import select

from src.database import SessionDep
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.models import User
from src.users.schemas import UserInSchema, UserOutSchema

router = APIRouter()


@router.get("")
async def get_all_users(session: SessionDep):
    stmt = select(User)
    users = session.exec(stmt).all()
    return users


# @router.post("/sign-up", response_model=UserOutSchema)
@router.post("/sign-up")
async def sign_up(user: UserInSchema, session: SessionDep) -> User:
    hashed_password = get_password_hash(user.password)
    user = User(username=user.username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/sign-in")
async def sign_in(response: Response, user_data: UserInSchema):
    """ Login user """
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"subject": user.id})
    # httponly=True important for safety!!!
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout(session: SessionDep):
    return ...