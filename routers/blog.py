from fastapi import APIRouter, HTTPException, Request, Depends, status
from blog.models import Post, Comment, User
from blog.database import db_session
from schemas.post import CreateBlogPost, UpdateBlogPost
from schemas.comment import CommentOnPost, UpdateComment
from utils.utils import get_username_by_id, post_owner, comment_owner, get_user_id_from_token
from blog.errors import UnauthorizedUser, PostNotFound, DeletedSuccessfully

from uuid import uuid4
from jwt import InvalidTokenError
import jwt
import os

blog = APIRouter(prefix="/api/blog", tags=["Blog Operations"])


def verify_token(req: Request):
    token = req.headers["Authorization"] if "Authorization" in req.headers else False

    if token is False:
        return False

    try:
        jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256")
        return True

    except InvalidTokenError:
        return False


@blog.post("/")
def create_blog_post(blog_post: CreateBlogPost, req: Request, authorized: bool = Depends(verify_token)):
    if not authorized:
        raise UnauthorizedUser

    user_id = get_user_id_from_token(req.headers["Authorization"])

    post_id = uuid4()

    if blog_post.title == "":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Missing form items.")

    post = Post(post_id, title=blog_post.title, post_author=user_id, post_content=blog_post.content)

    db_session.add(post)
    db_session.commit()

    return {
        "msg": "Post created successfully.",
        "id": post_id
    }


@blog.get("/{post_id}")
def get_blog_post(post_id: str):
    post = db_session.query(Post).filter(Post.post_id == post_id).first()
    if post:
        post.views += 1

        comments = db_session.query(Comment).filter(Comment.post_id == post_id).all()

        author = get_username_by_id(post.post_author)

        return {
            "title": post.title,
            "post_content": post.post_content,
            "post_author": author,
            "post_id": post.post_id,
            "views": post.views,
            "date_created": post.date_created,
            "Comments": {
                get_username_by_id(comment.user_id): comment.comment for comment in comments
            } if comments != [] else comments
        }

    raise PostNotFound


@blog.get("/get-all-posts")
def get_all_blog_posts():
    posts = db_session.query(Post).all()
    return posts


@blog.patch("/update/{post_id}")
def update_blog_post(post_id, post: UpdateBlogPost, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])

        post_to_update = db_session.query(Post).get(post_id)

        if not post_to_update:
            raise PostNotFound

        if not post_owner(user_id, post_id):
            raise UnauthorizedUser

        # Update the attributes dynamically based on the provided values
        for attr, value in post.dict().items():
            if value is not None:
                setattr(post_to_update, attr, value)

        db_session.commit()

        return {
            "msg": "Updated successfully."
        }

    raise UnauthorizedUser


@blog.delete("/delete/{post_id}")
def delete_blog_post(post_id, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])

        post = db_session.query(Post).get(post_id)
        if not post:
            raise PostNotFound

        if post_owner(user_id, post_id):
            db_session.delete(post)
            db_session.commit()

            raise DeletedSuccessfully

        raise UnauthorizedUser

    raise UnauthorizedUser


@blog.post("/comment/{post_id}")
def comment_on_blog_post(post_id, comment: CommentOnPost, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])
        comment_id = uuid4()
        if comment.content == "":
            raise HTTPException(400, "Comment cannot be empty.")

        comment_obj = Comment(comment_id, comment.content, user_id, post_id)

        db_session.add(comment_obj)
        db_session.commit()

        return {
            "msg": "Comment created",
            "comment_id": comment_id
        }

    raise UnauthorizedUser


@blog.patch("/comment/update/{comment_id}")
def update_comment(comment_id, comment: UpdateComment, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])

        comment_to_update = db_session.query(Comment).get(comment_id)

        if not comment_to_update:
            raise HTTPException(status_code=400, detail="Comment does not exist in the database.")

        if comment_owner(user_id, comment_id):
            # Update the attributes dynamically based on the provided values
            comment_to_update.comment = comment.content
            db_session.commit()

            return {
                "msg": "Comment updated successfully",
                "comment_id": comment_id
            }
        raise UnauthorizedUser

    raise UnauthorizedUser


@blog.delete("/comment/delete/{comment_id}")
def delete_comment(comment_id, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])
        comment = db_session.query(Comment).get(comment_id)

        if not comment:
            raise HTTPException(404, "Comment does not exist.")

        if comment_owner(user_id, comment_id):
            db_session.delete(comment)
            db_session.commit()
            raise DeletedSuccessfully

        raise UnauthorizedUser

    raise UnauthorizedUser
