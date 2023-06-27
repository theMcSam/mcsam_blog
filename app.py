from fastapi import FastAPI
from routers.auth import auth

app = FastAPI()

@app.get("/")
def web_root():
    return {
        "msg" : "Welcome to McSam's blog"
    }

app.include_router(auth)