from fastapi import APIRouter, status

from blog.errors import IncorrectUsernameOrPassword, DuplicateUsernames, DuplicateEmails
from schemas.auth import UserLogin, UserSignUp
from blog.database import db_session
from blog.models import User

from uuid import uuid4
import os
import bcrypt
import jwt

auth = APIRouter(prefix="/api/auth", tags=["Authentication"])
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


@auth.post("/login")
def login(user: UserLogin):
    user_obj = db_session.query(User).filter(User.username == user.username).first()

    if user_obj and bcrypt.checkpw(user.password.encode(), str(user_obj.password).encode()):
        jwt_payload = {"username": user.username, "user_id": str(user_obj.user_id)}

        token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm="HS256")

        return {
            "msg": "Logged in successfully.",
            "user_id": user_obj.user_id,
            "token": token
        }

    raise IncorrectUsernameOrPassword(
        status.HTTP_404_NOT_FOUND,
        detail="Incorrect username or password."
    )


@auth.post("/signup")
def sign_up(user: UserSignUp):
    username_exists = db_session.query(User).filter(User.username == user.username).first()

    if username_exists:
        raise DuplicateUsernames(
            status.HTTP_400_BAD_REQUEST,
            detail="Duplicate usernames not allowed."
        )

    email_exists = db_session.query(User).filter(User.email == user.email).first()

    if email_exists:
        raise DuplicateEmails(
            status.HTTP_400_BAD_REQUEST,
            detail="Duplicate email not allowed."
        )

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt(12)).decode()

    user = User(username=user.username, password=hashed_password, email=user.email)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "date_created": user.date_created
    }
