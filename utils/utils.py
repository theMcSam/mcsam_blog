from blog.database import db_session
from blog.models import User, Post, Comment

import jwt
import os

def get_username_by_id(id: str):
    user = db_session.query(User).filter(User.user_id == id).first()

    if user:
        return user.username
    
    return ""

def post_owner(user_id, post_id):
    post = db_session.query(Post).filter(Post.post_id == post_id).first()

    if not post:
        return False

    if post.post_author == user_id:
        return True
    
    return False

def comment_owner(user_id, comment_id):
    comment = db_session.query(Comment).filter(Comment.comment_id == comment_id).first()

    if not comment:
        return False

    if  comment.user_id == user_id:
        return True
    
    return False

def account_owner(user_id, account_id):
    user = db_session.query(User).filter(User.user_id == user_id).first()

    if not user:
        return False

    if user.user_id == account_id:
        return True
    
    return False


def get_user_id_from_token(token):
    jwt_payload = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256")

    user_id = jwt_payload["user_id"]

    return user_id