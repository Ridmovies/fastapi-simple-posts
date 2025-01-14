from fastapi import APIRouter, Response

from src.users.auth import UserDep, login
from src.users.schemas import UserInSchema, UserOutSchema
from src.users.service import UserService

router = APIRouter()


@router.get("", response_model=list[UserOutSchema])
async def get_all_users():
    return UserService.get_all_users()


@router.post("/sign-up", response_model=UserOutSchema)
async def sign_up(user: UserInSchema):
    return UserService.add_user(user)


@router.post("/sign-in")
async def sign_in(response: Response, user_data: UserInSchema):
    """ Login user """
    return login(response, user_data)


@router.post("/logout")
async def logout(response: Response):
    """ Logout user """
    response.delete_cookie(key="access_token")
    return {"message": "logout"}


@router.get("/me")
async def get_current_user(current_user: UserDep):
    return current_user

