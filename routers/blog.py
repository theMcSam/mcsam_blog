from fastapi import APIRouter

blog = APIRouter()

@blog.post("/api/blog/create-post")
def create_blog_post():
    ...

@blog.get("/api/blog/get-post/{post_id}")
def get_blog_post():
    ...

@blog.get("/api/blog/get-all-posts")
def get_all_blog_posts():
    ...

@blog.put("/api/blog/update/{post_id}")
def update_blog_post():
    ...

@blog.delete("/api/blog/delete/{post_id}")
def delete_blog_post():
    ...

@blog.post("/api/blog/comment/{post_id}")
def comment_on_blog_post():
    ...

