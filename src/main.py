from fastapi import FastAPI

from src.posts.routers import router as posts_router
from src.users.routers import router as user_router
from src.dev.routers import router as dev_router

app = FastAPI()

app.include_router(posts_router, prefix='/posts', tags=['Posts'])
app.include_router(user_router, prefix='/users', tags=['Users'])
app.include_router(dev_router, prefix='/dev', tags=['Dev'])




