from pydantic import BaseModel
from typing import Optional


class CreateBlogPost(BaseModel):
    title: str
    content: str


class UpdateBlogPost(BaseModel):
    title: Optional[str]
    content: Optional[str]
