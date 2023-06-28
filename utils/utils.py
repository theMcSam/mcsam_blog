from blog.database import db_session
from blog.models import User, Post, Comment

import jwt
import os

async def get_username_by_id(id: str):
    user = await db_session.query(User).filter(User.user_id == id).first()

    if user:
        return user.username
    
    return ""

async def post_owner(user_id, post_id):
    post = await db_session.query(Post).filter(Post.post_id == post_id).first()

    if post.post_author == user_id:
        return True
    
    return False

async def comment_owner(user_id, comment_id):
    comment = await db_session.query(Comment).filter(Comment.comment_id == comment_id).first()

    if  comment.user_id == user_id:
        return True
    
    return False

async def account_owner(user_id, account_id):
    user = await db_session.query(User).filter(User.user_id == user_id).first()

    if user.user_id == account_id:
        return True
    
    return False


def get_user_id_from_token(token):
    jwt_payload = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256")

    user_id = jwt_payload["user_id"]

    return user_id