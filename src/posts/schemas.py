from pydantic import BaseModel

class PostInSchema(BaseModel):
    content: str
    user_id: int