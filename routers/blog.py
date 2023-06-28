from fastapi import APIRouter, HTTPException, Request, Depends
from blog.models import Post, Comment, User
from blog.database import db_session
from schemas.post import CreateBlogPost, UpdateBlogPost
from schemas.comment import CommentOnPost, UpdateComment
from utils.utils import get_username_by_id, post_owner, comment_owner, get_user_id_from_token

from uuid import uuid4
from jwt import InvalidTokenError
import jwt
import os

blog = APIRouter()

def verify_token(req: Request):
    token = req.headers["Authorization"] if "Authorization" in req.headers else False

    if token is False:
        return False

    try:
        jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256")
        return True

    except InvalidTokenError:
        return False

@blog.post("/api/blog/create-post")
def create_blog_post(blog_post: CreateBlogPost, req: Request,authorized: bool = Depends(verify_token)):
    if not authorized:
        raise HTTPException(status_code=403, detail="You are not authorized to make this request.")
    
    user_id = get_user_id_from_token(req.headers["Authorization"])

    post_id = uuid4()

    if blog_post.title == "" :
        raise HTTPException(400, "Missing form items.")
    
    post = Post(post_id, title=blog_post.title, post_author=user_id, post_content=blog_post.content)

    db_session.add(post)
    db_session.commit()

    return {
        "msg": "Post created successfully.",
        "id" : post_id
        }

@blog.get("/api/blog/get-post/{post_id}")
def get_blog_post(post_id: str):
    post = db_session.query(Post).filter(Post.post_id == post_id).first()
    if post:
        post.views += 1

        comments = db_session.query(Comment).filter(Comment.post_id == post_id).all()
        author = get_username_by_id(post.post_author)
        if comments != []:
            return {
                    "title": post.title,
                    "post_content": post.post_content,
                    "post_author": author,
                    "post_id": post.post_id,
                    "views": post.views,
                    "date_created": post.date_created,
                    "Comments": {
                        get_username_by_id(comment.user_id): comment.comment for comment in comments
                        },    
            }
        return {
                "title": post.title,
                "post_content": post.post_content,
                "post_author": author,
                "post_id": post.post_id,
                "views": post.views,
                "date_created": post.date_created,   
            }
    
    raise HTTPException(400, "Post not found in database.")

@blog.get("/api/blog/get-all-posts")
def get_all_blog_posts():
    posts =  db_session.query(Post).all()
    return posts

@blog.put("/api/blog/update/{post_id}")
def update_blog_post(post_id, post: UpdateBlogPost, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        token = req.headers["Authorization"]
        jwt_payload = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms="HS256")

        user_id = jwt_payload["user_id"]

        if not post_owner(user_id, post_id):
            raise HTTPException(403, "You do now own this post.")
        
        post_to_update = db_session.query(Post).get(post_id)

        if not post_to_update:
            raise HTTPException(status_code=400, detail="Post does not exist in the database")

        # Update the attributes dynamically based on the provided values
        for attr, value in post.dict().items():
            if value is not None:
                setattr(post_to_update, attr, value)

        db_session.commit()

        return {
            "msg": "Updated successfully."
            }
    
    raise HTTPException(403, "You are not authorized.")
            

@blog.delete("/api/blog/delete/{post_id}")
def delete_blog_post(post_id, req:Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])

        if post_owner(user_id, post_id):
            post =  db_session.query(Post).get(post_id)
            if post:
                db_session.delete(post)
                db_session.commit()

                raise HTTPException(201, "Post deleted successfully.")
            
            raise HTTPException(404, "Post does not exist.")
        
        raise HTTPException(403, "You do not own this post.")
    
    raise HTTPException(403, "You are not authorized to perform this action.")


@blog.post("/api/blog/comment/{post_id}")
def comment_on_blog_post(post_id, comment: CommentOnPost, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])
        comment_id = uuid4()
        if comment.content == "":
            raise HTTPException(400, "Comment cannot be empty.")
        
        comment_obj = Comment(comment_id, comment.content, user_id, post_id)

        db_session.add(comment_obj)
        db_session.commit()

        raise HTTPException(201, "Comment created")
    
    raise HTTPException(403, "You are not authorized to perform this action.")

@blog.put("/api/blog/comment/update/{comment_id}")
def update_comment(comment_id, comment: UpdateComment, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])

        if comment_owner(user_id, comment_id):
            comment_to_update =  db_session.query(Comment).get(comment_id)

            if not comment_to_update:
                raise HTTPException(status_code=400, detail="Comment does not exist in the database.")

            # Update the attributes dynamically based on the provided values
            for attr, value in comment.dict().items():
                if value is not None:
                    setattr(comment_to_update, attr, value)

            db_session.commit()

            return {
                "msg": "Comment updated successfully",
                "comment_id": comment_id 
                }
        raise HTTPException(403, "You do not own this comment.")
    
    raise HTTPException(403, "You are not authorized to perform this action.")

@blog.delete("/api/blog/comment/delete/{comment_id}")
def delete_comment(comment_id, req: Request, authorized: bool = Depends(verify_token)):
    if authorized:
        user_id = get_user_id_from_token(req.headers["Authorization"])

        if comment_owner(user_id, comment_id):
            comment =  db_session.query(Comment).get(comment_id)

            if comment:
                db_session.delete(comment)
                db_session.commit()
                raise HTTPException(204, "Comment deleted successfully.")
            
            raise HTTPException(404, "Comment does not exist.")
        
        raise HTTPException(403, "You are not authorized to perform this action.")
    
    raise HTTPException(403, "You are not authorized to perform this action.")


