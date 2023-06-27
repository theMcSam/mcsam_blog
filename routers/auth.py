from fastapi import APIRouter

auth = APIRouter()

@auth.post("/api/auth/login")
def login():
    ...