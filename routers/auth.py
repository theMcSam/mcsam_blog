from fastapi import APIRouter, HTTPException
from schemas.auth import UserLogin, UserSignUp
from blog.database import db_session
from blog.models import User

from uuid import uuid4
import os
import bcrypt
import jwt
import dotenv


auth = APIRouter()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

@auth.post("/api/auth/login")
def login(user: UserLogin):
    user_obj = db_session.query(User).filter(User.username == user.username).first()

    if user_obj and bcrypt.checkpw(user.password.encode(), str(user_obj.password).encode()):
        jwt_payload = {"username": user.username, "user_id": user_obj.user_id}
        print(f"-----------\n{JWT_SECRET_KEY}\n------------------")
        token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm="HS256")

        return {
            "msg":"Logged in successfully.",
            "user_id": user_obj.user_id,
            "token": token
        }
       

    raise HTTPException(status_code=404, detail="Username or password is incorrect.")

@auth.post("/api/auth/signup")
def sign_up(user: UserSignUp):
    user_id = str(uuid4())

    username_exists = db_session.query(User).filter(User.username == user.username).first()

    if username_exists:
        raise HTTPException(status_code=400, detail="Duplicate usernames not allowed.")

    email_exists = db_session.query(User).filter(User.email == user.email).first()

    if  email_exists:
        raise HTTPException(status_code=400, detail="Email already exits.")
    
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt(12)).decode()

    user = User(user_id, user.username, hashed_password, user.email)
    db_session.add(user)
    db_session.commit()

    return {
        "msg" : "User registered successfully."
    }