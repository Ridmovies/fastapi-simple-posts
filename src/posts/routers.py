from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.database import SessionDep
from src.posts.models import Post

router = APIRouter()

@router.get("")
async def get_all_posts(session: SessionDep):
    statement = select(Post)
    posts = session.exec(statement).all()
    return posts


@router.get("{post_id}")
async def get_post_by_id(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("")
async def create_post(post: Post, session: SessionDep):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.delete("{post_id}")
async def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"ok": True}