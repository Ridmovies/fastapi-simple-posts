from fastapi import APIRouter, HTTPException

from src.database import SessionDep
from src.posts.models import Post
from src.posts.service import PostService
from src.users.auth import UserDep

router = APIRouter()


@router.get("")
async def get_all_posts():
    return PostService.get_all()


@router.get("/{post_id}")
async def get_post_by_id(post_id: int):
    return PostService.get_one_by_id(post_id)


@router.get("/{user_id}")
async def get_post_by_user_id(user_id: int):
    return PostService.get_one_or_none(user_id)


# @router.post("")
# async def create_post(post: Post, user: UserDep, session: SessionDep):
#     post = Post(**post.model_dump(), user_id=user.id)
#     session.add(post)
#     session.commit()
#     session.refresh(post)
#     return post

@router.post("")
async def create_post(post: Post, user: UserDep, session: SessionDep):
    return PostService.create(post)


# @router.delete("{post_id}")
# async def delete_post(post_id: int, user: UserDep, session: SessionDep):
#     post = session.get(Post, post_id)
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     if post.user_id != user.id:
#         raise HTTPException(status_code=403, detail="You are not the owner of this post")
#     session.delete(post)
#     session.commit()
#     return {"ok": True}

@router.delete("/{post_id}")
async def delete_post(post_id: int, user: UserDep, session: SessionDep):
    return PostService.delete(post_id)


@router.put("/{post_id}")
async def update_post(post_id: int, post: Post, user: UserDep):
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this post")
    return PostService.update(post_id, post)


@router.patch("/{post_id}")
async def update_post(post_id: int, post: Post, user: UserDep):
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this post")
    return PostService.patch(post_id, post)