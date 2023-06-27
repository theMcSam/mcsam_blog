from fastapi import APIRouter
from schemas.auth import UserLogin

auth = APIRouter()

@auth.post("/api/auth/login")
def login(user: UserLogin):
    ...