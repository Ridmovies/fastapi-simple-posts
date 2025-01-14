from sqlmodel import SQLModel, Field, Relationship

from src.auth.auth import User


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="posts")