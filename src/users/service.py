from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.database import engine
from src.users.auth import get_password_hash
from src.users.models import User
from src.users.schemas import UserInSchema


class UserService:
    @classmethod
    def add_user(cls, user: UserInSchema):
        with Session(engine) as session:
            hashed_password = get_password_hash(user.password)
            try:
                user = User(username=user.username, hashed_password=hashed_password)
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


    @classmethod
    def get_all_users(cls):
        with Session(engine) as session:
            stmt = select(User)
            users = session.exec(stmt).all()
            return users