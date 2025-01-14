from sqlmodel import SQLModel, Field, Relationship

from src.posts.models import Post


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str

    posts: list["Post"] = Relationship(back_populates="user")