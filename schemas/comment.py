from pydantic import BaseModel
from typing import Optional

class CommentOnPost(BaseModel):
    content: str

class UpdateComment(BaseModel):
    content: Optional[str]
