from fastapi import FastAPI
from routers.auth import auth
from routers.blog import blog

app = FastAPI()

@app.get("/")
def web_root():
    return {
        "msg" : "Welcome to McSam's blog"
    }

app.include_router(auth)
app.include_router(blog)