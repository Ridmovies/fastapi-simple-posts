from services import BaseService
from src.posts.models import Post


class PostService(BaseService):
    model = Post