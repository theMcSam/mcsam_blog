from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def web_root():
    return {
        "msg" : "Welcome to McSam's blog"
    }